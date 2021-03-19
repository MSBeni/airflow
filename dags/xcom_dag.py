from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.operators.subdag import SubDagOperator
from airflow.utils.task_group import TaskGroup

from random import uniform
from datetime import datetime


def _training_model():
    accuracy = uniform(0.1, 10.0)
    return f'model\'s accuracy is {accuracy}'


def _choose_best_model():
    print("Choose Best Model")


default_args = {
    'start_sate': datetime(2020, 1, 1)
}
with DAG(dag_id='xcom_dag', schedule_interval='@daily', default_args=default_args, catchup=False) as dag:
    pass
