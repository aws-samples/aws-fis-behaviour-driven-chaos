import logging
from step_helpers.locust_helper import send_traffic_to_website
from step_helpers.pandas_helper import verify_locust_run, success_percent

logger = logging.getLogger(__name__)


@step("My website is up and can serve {number} transactions per second")
def step_impl(context, number):

    target = f"http://{context.config.userdata['website_hostname']}"

    logger.info(f'Sending traffic to target website: {target} for the next 60 seconds, please wait....')
    send_traffic_to_website(target, 60, "before_chaos", int(number))

    assert verify_locust_run(int(number), "before_chaos") is True


@step("I can continue to serve {number} transactions per second")
def step_impl(context, number):

    target = f"http://{context.config.userdata['website_hostname']}"

    logger.info(f'Sending traffic to target website {target} for the next 60 seconds, please wait....')
    send_traffic_to_website(target, 60, "after_chaos", int(number))

    assert verify_locust_run(int(number), "after_chaos") is True


@step("{percentage} percent of transactions to my website succeed")
def step_impl(context, percentage):

    assert success_percent(int(percentage), "after_chaos") is True
