import json
import os.path
import locust  # imported here to prevent issues with SSL later......


def before_all(context):
    """Load and update userdata from JSON configuration file."""
    userdata = context.config.userdata
    configfile = userdata.get("configfile", "userconfig.json")
    if os.path.exists(configfile):
        assert configfile.endswith(".json")
        more_userdata = json.load(open(configfile))
        context.config.update_userdata(more_userdata)

    """Create the clients key in context"""
    context.clients = {}

    # '''Setup logging'''
    # context.config.setup_logging()
    # context.logger = logging.getLogger(__name__)
