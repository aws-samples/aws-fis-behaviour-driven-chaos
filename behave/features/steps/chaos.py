import logging
from step_helpers.fis_helper import start_experiment
from step_helpers.clients import create_client

logger = logging.getLogger(__name__)


@step("an EC2 instance is lost")
def step_impl(context):

    if "fis" not in context.clients:
        create_client("fis", context)

    state = start_experiment(
        context.clients["fis"], context.config.userdata["fis_experiment_id"]
    )["experiment"]["state"]["status"]
    logger.info(f"FIS experiment state is: {state}")

    assert state in ["running", "initiating"]
