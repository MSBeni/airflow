from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

default_args = {
    'start_date': datetime(2020, 1, 1)
}

with DAG(dag_id='parallel_dag', schedule_interval='@daily', default_args=default_args , catchup=False):
    # Extract the user from api
    task_1 = BashOperator(
        task_id='task_1',
        bash_command='sleep 3'
    )

    task_2 = BashOperator(
        task_id='task_2',
        bash_command='sleep 3'
    )

    task_3 = BashOperator(
        task_id='task_3',
        bash_command='sleep 3'
    )