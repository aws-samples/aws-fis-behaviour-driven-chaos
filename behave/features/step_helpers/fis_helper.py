import logging
from random import randrange

logger = logging.getLogger(__name__)


def start_experiment(client, template_id: str) -> None:
    """
    Start the FIS experiment with the given template ID
    """

    client_token = str(randrange(10000, 50000))

    # we should poll for experiment completion here whilst in a separate
    # thread have still running to validate txn rate or whatever
    # during the experiment run.....
    return client.start_experiment(
        clientToken=client_token, experimentTemplateId=template_id
    )
