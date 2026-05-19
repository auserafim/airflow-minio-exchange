import sys

sys.path.append("/opt/airflow")

from datetime import datetime

from airflow.decorators import task
from airflow.providers.standard.operators.empty import EmptyOperator
from airflow.sdk import DAG, get_current_context

with DAG(
    dag_id="Main-Orchestration",
    description="Dag that will clean the datasets and make them available to training",
    start_date=datetime(2025, 1, 13),
    catchup=False,
    is_paused_upon_creation=False,
    tags=["Main Orchestration"],
    schedule=None,
) as dag:
    start = EmptyOperator(task_id="start")

    @task(task_id="fetching_data")
    def run_fetching_data():

        context = get_current_context()

        conf = context["dag_run"].conf

        key = conf["key"]
        event_time = conf["event_time"]
        event_name = conf["event_name"]

        print(key)
        print(event_time)
        print(event_name)
        print("things did not work")

    end = EmptyOperator(task_id="end")

    start >> run_fetching_data() >> end
