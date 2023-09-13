# This is based on https://docs.locust.io/en/stable/use-as-lib.html - this is experimental and should not be 'productionised'

# Enhancement: Run Locust as a separate thread to the rest of the Behave test steps and be running whilst those are executing then be stopped
# after the Chaos step(s) have run to allow for evaluation of the results.
import gevent
from locust import HttpUser, task, events
from locust.env import Environment
from locust.stats import stats_printer, stats_history, StatsCSVFileWriter
from locust.log import setup_logging

setup_logging("INFO", None)


def send_traffic_to_website(
    target_host: str, duration: int, file_prefix: str, transaction_rate: int
) -> None:
    """
    Invoke a local Locust runner for the number of seconds
    indicated by duration
    """

    class MyUser(HttpUser):
        host = target_host

        @task
        def t(self):
            self.client.get("/")

    # setup Environment and Runner
    locust_env = Environment(user_classes=[MyUser], events=events)
    runner = locust_env.create_local_runner()

    csv_writer = StatsCSVFileWriter(
        locust_env,
        base_filepath=f"./{file_prefix}-locust_results",
        percentiles_to_report=[1.0],
        full_history=True,
    )

    # execute init event handlers (only really needed if you have registered any)
    locust_env.events.init.fire(environment=locust_env, runner=runner)

    gevent.spawn(csv_writer)

    # start a greenlet that save current stats to history
    gevent.spawn(stats_history, locust_env.runner)

    # start the test
    runner.start(transaction_rate, spawn_rate=transaction_rate, wait=True)

    # in 30 seconds stop the runner
    gevent.spawn_later(duration, lambda: runner.quit())

    # wait for the greenlets
    runner.greenlet.join()

    csv_writer.close_files()
