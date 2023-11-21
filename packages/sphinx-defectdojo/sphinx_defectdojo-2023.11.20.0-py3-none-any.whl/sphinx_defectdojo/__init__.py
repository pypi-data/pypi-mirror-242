from .finding import DojoFinding

from sphinx.application import Sphinx

def setup(app: Sphinx):
    """
    Extension setup, called by Sphinx
    """

    app.add_directive('dojofinding', DojoFinding)

    app.add_config_value("dojo_host", None, rebuild="env")
    app.add_config_value("dojo_token", None, rebuild="env")