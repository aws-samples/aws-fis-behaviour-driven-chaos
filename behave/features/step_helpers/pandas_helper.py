import pandas as pd
import logging

logger = logging.getLogger(__name__)


def verify_locust_run(transaction_rate: int, file_prefix: str) -> bool:
    """
    Verify number of requests to confirm we are generating
    sufficient load to meet our defined steady state
    """

    df = pd.read_csv(f"./{file_prefix}-locust_results_stats.csv")
    if int(df["Requests/s"][0] - df["Failures/s"][0]) >= transaction_rate:
        return True

    return False


def success_percent(required_percentage: int, file_prefix: str) -> bool:
    """
    Verify number of successful requests to our website
    does not drop below the percentage defined by the percentage argument
    """

    df = pd.read_csv(f"./{file_prefix}-locust_results_stats.csv")
    failure_proportion = float(df["Failure Count"][0] / df["Request Count"][0])
    success_percent = (1 - failure_proportion) * 100
    logger.info(f"Successful request percentage: {success_percent}%")
    if success_percent >= required_percentage:
        return True

    return False
