from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.operators.subdag import SubDagOperator
from airflow.utils.task_group import TaskGroup

from random import uniform
from datetime import datetime

def _tarining_model():
    pass

default_args = {
    'start_sate': datetime(2020, 1, 1)
}
with DAG(dag_id='xcom_dag', schedule_interval='@daily', default_args=default_args, catchup=False) as dag:
    pass
