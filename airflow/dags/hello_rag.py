"""A first DAG: proves Airflow can schedule and run our Python code."""

from datetime import datetime

from airflow.sdk import dag, task


@dag(
    schedule=None,
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=["phase-1"],
)
def hello_rag():
    @task
    def say_hello() -> str:
        message = "Airflow is running"
        print(message)
        return message

    @task
    def shout(message: str) -> None:
        print(message.upper())

    shout(say_hello())


hello_rag()