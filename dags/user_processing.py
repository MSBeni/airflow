from airflow.models import DAG
from airflow.providers.sqlite.operators.sqlite import SqliteOperator
from airflow.providers.http.sensors.http import HttpSensor
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.operators.python import PythonOperator

from datetime import datetime
import json

default_args = {
    'start_date': datetime(2020, 1, 1)
}


def _processing_user():
    pass


# each DAG out to has a unique dag_id
with DAG(dag_id='user_processing', schedule_interval='@daily', default_args=default_args, catchup=False) as dag:
    # define tasks/operators
    creating_table = SqliteOperator(
        task_id='creating_table',        # Ought to be unique -- each task one unique id
        sqlite_conn_id='db_sqlite',
        sql='''
            CREATE TABLE users (
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                country TEXT NOT NULL,
                user_name TEXT NOT NULL,
                password TEXT NOT NULL,
                email TEXT NOT NULL PRIMARY KEY     
            );
        '''
    )

    is_api_available = HttpSensor(
        task_id='is_api_available',
        http_conn_id='user_api',
        endpoint='api/'
    )

    # Extract the user from api
    extracting_user = SimpleHttpOperator(
        task_id='user_extraction',
        http_conn_id='user_api',
        endpoint='api/',
        method='GET',
        response_filter=lambda response: json.loads(response.text),
        log_response=True
    )

    processing_user = PythonOperator(
        task_id='processing_user',
        python_callable=_processing_user
    )




    