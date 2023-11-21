import string

from collections import defaultdict


from docutils.parsers.rst import directives, Directive, Parser
from docutils.parsers.rst.directives.tables import ListTable
from docutils import nodes, utils, frontend
from docutils.utils import SystemMessagePropagation, Reporter


import sphinx
from sphinx.util import logging
from sphinx.application import Sphinx

import dojo


class DojoFinding(ListTable, Directive):
    """
    Example of the directive:

    .. code-block:: rest

      .. dojofinding::
         :finding: 20

      .. dojofinding::
         :testid: 20
         
      .. dojofinding::
         :productname: somename

    """

    _header_spec = {"id": {"template": string.Template("`${id} <${host}/finding/${id}>`__")},
                    "date": {"title": "Date"},
                    "status": {"fromfield": "display_status"},
                    "jira": {"title": "Jira",
                             "fromobj": "jira",
                             "template": string.Template("`${jira_key} <${url}>`__"),
                             "default": "None"},
                    "vulnerability_id": {"title": "CVE",
                                         "fromfield": "vuln_id_from_tool"},
                    "severity": {},
                    "sla": {"title": "SLA",
                            "fromfield": "sla_days_remaining"},
                    "title": {}
                    }



    has_content = False


    option_spec = {

        'finding': directives.unchanged_required,
        'testid': directives.unchanged_required,
        'product_name': directives.unchanged_required
    }


    def run(self):
        """
        Implements the directive
        """

        env = self.state.document.settings.env  # sphinx.environment.BuildEnvironment 
        config = env.config

        host = config["dojo_host"]
        token = config["dojo_token"]


        # Get content and options
        finding = self.options.get('finding', None)
        testid = self.options.get('testid', None)
        product_name = self.options.get('product_name', None)

        header_rows = 1
        stub_columns = 0

        col_widths = [5,5,5,5,5,5,5,65]

        if finding is None and testid is None and product_name is None:
            return [self._report(u"No Finding, test or productname given")]
        if host is None:
            return [self._report(u"No dojo_host set in configuration")]
        if token is None:
            return [self._report(u"No dojo_token set in configuration")]
        

        list_of_findings = self.get_findings(finding=finding, testid=testid, product_name=product_name,
                                             host=host, token=token)

        header_row = list()

        for header in self._header_spec.keys():
            hdef = self._header_spec[header]
            this_header = nodes.paragraph(text=hdef.get("title", header.capitalize()))
            header_row.append(this_header)
        
        table_body = list()

        for this_finding in list_of_findings:
            this_row = self.gen_finding_row(this_finding=this_finding, host=host)

            table_body.append(this_row)

        table_data = [header_row, *table_body]

        table_node = self.build_table_from_list(table_data, col_widths=col_widths, header_rows=1, stub_columns=0)

        return [table_node]
    
    def gen_finding_row(self, this_finding, host=None):

        this_row = list()

        for header in self._header_spec.keys():
            hdef = self._header_spec[header]
            fromobj = hdef.get("fromobj", "finding")
            fromfield = hdef.get("fromfield", header)

            if this_finding[fromobj].data is None:
                this_data = "None"
            elif fromfield not in this_finding[fromobj].data.keys() and hdef.get("template", None) is None:
                print("missing {} {}".format(fromobj, fromfield))
                this_data = "None"
            elif hdef.get("template", None) is not None:
                this_data = hdef["template"].safe_substitute(**this_finding[fromobj].data, host=host)
            else:
                this_data = this_finding[fromobj].data[fromfield]
            
            default_settings = frontend.OptionParser(
                components=(Parser,)).get_default_values()
            document = utils.new_document("", default_settings)
            parser = Parser()

            parser.parse(str(this_data), document)

            n = document.traverse()[1]

            this_row.append(n)
        
        return this_row
    
    
    def get_findings(self, finding=None, testid=None, product_name=None, host=None, token=None):

        list_of_findings = list()
        list_of_finding_ids = list()
        filters_to_get = list()

        if testid is not None:
            all_testids = self.simple_expand(testid, castto="int")

            for id in all_testids:
                this_filter = {"test": id}
                filters_to_get.append(this_filter)

        if product_name is not None:
            all_product_names = self.simple_expand(product_name, castto="str")

            for product_name in all_product_names:
                this_filter = {"product_name": product_name}
                filters_to_get.append(this_filter)
        
        if finding is not None:
            all_finding_ids = self.simple_expand(finding, castto="int")

            for finding_id in all_finding_ids:
                this_filter = {"id": finding_id}
                filters_to_get.append(this_filter)

        for this_filter in filters_to_get:

            vulns = dojo.api_multi(type=dojo.Finding, data=this_filter, host=host, token=token)

            for vuln in vulns.data["results"]:
                if int(vuln["id"]) not in list_of_finding_ids:
                    # Prevents Duplicates
                    list_of_finding_ids.append(int(vuln["id"]))

                    this_finding = dojo.Finding(id=vuln["id"], action="get", host=host, token=token)
                    if this_finding.id is not None:
                        this_jira_mapping = dojo.Jira_Findings_Mapping(data={"finding": this_finding.id}, action="search", host=host, token=token)
                    else:
                        this_jira_mapping = None
                    
                    list_of_findings.append({"finding": this_finding, "jira": this_jira_mapping})
                else:
                    # This is a Duplicate Finding Ignore and continue
                    pass
        
        return list_of_findings


    def simple_expand(self, thing, castto="int"):

        expanded = list()

        if "," in thing:
            things = thing.split(",")
        else:
            things = [thing]
        
        for onething in things:
            if onething.count(":") == 1 and castto =="int":
                # It's a range of things
                start = onething.split(":")[0]
                end = onething.split(":")[1]
                allthings = list(range(int(start), int(end)+1))
                expanded.extend(allthings)
            else:
                # It's just one thing place it on the list
                if castto == "int":
                    expanded.append(int(onething))
                else:
                    expanded.append(onething)
        


        return list(set(expanded))



