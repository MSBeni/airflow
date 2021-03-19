from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
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
    downloading_date = BashOperator(
        task_id='downloading_date',
        bash_command='sleep 3'
    )

    with TaskGroup('processing_tasks') as processing_tasks:
        training_model_1 = PythonOperator(
            task_id='training_model_1',
            python_callable=_training_model
        )
        training_model_2 = PythonOperator(
            task_id='training_model_2',
            python_callable=_training_model
        )
        training_model_3 = PythonOperator(
            task_id='training_model_3',
            python_callable=_training_model
        )

    chosen_model = PythonOperator(
        task_id='chosen_model',
        bash_command=_choose_best_model
    )

    downloading_date >> processing_tasks >> chosen_model

