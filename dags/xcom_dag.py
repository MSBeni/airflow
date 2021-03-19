from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.operators.bash import BashOperator
from airflow.utils.task_group import TaskGroup

from random import uniform
from datetime import datetime


def _training_model(ti):
    accuracy = uniform(0.1, 10.0)
    print(f'model\'s accuracy is {accuracy}')
    return ti.xcom_push(key='model_accuracy', value=accuracy)


def _choose_best_model(ti):
    print("Choose Best Model")
    accuracies = ti.xcom_pull(key='model_accuracy', task_ids=[
        'processing_tasks.training_model_a',
        'processing_tasks.training_model_b',
        'processing_tasks.training_model_c',
    ])
    print(accuracies)


def _is_accurate():
    return 'accurate'


default_args = {
    'start_date': datetime(2020, 1, 1)
}

with DAG('xcom_dag', schedule_interval='@daily', default_args=default_args, catchup=False) as dag:
    downloading_date = BashOperator(
        task_id='downloading_date',
        bash_command='sleep 3',
        do_xcom_push=False
    )

    with TaskGroup('processing_tasks') as processing_tasks:
        training_model_a = PythonOperator(
            task_id='training_model_a',
            python_callable=_training_model
        )

        training_model_b = PythonOperator(
            task_id='training_model_b',
            python_callable=_training_model
        )

        training_model_c = PythonOperator(
            task_id='training_model_c',
            python_callable=_training_model
        )

    choose_model = PythonOperator(
        task_id='choose_model',
        python_callable=_choose_best_model
    )

    is_accurate = BranchPythonOperator(
        task_id='is_accurate',
        python_callable=_is_accurate
    )

    accurate = DummyOperator(
        task_id='accurate'
    )

    downloading_date >> processing_tasks >> choose_model

