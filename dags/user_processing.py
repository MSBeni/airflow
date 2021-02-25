from airflow.models import DAG
from airflow.providers.sqlite.operators.sqlite import SqliteOperator
from airflow.providers.http.sensors.http import HttpSensor
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.operators.python import PythonOperator
from pandas import json_normalize
from datetime import datetime
import json

default_args = {
    'start_date': datetime(2020, 1, 1)
}


# when your task is triggered by the scheduler you can access a task instance (ti) object
def _processing_user(ti):
    users = ti.xcom_pull(task_ids=['user_extraction'])
    if not len(users) or 'results' not in users[0]:
        raise ValueError('User is Empty ...')

    user = users[0]['results']
    # Using json_normalize to create a dataframe from the dictionary
    processed_user = json_normalize({
        'first_name': user['name']['first'],
        'last_name': user['name']['last'],
        'country': user['location']['country'],
        'user_name': user['login']['username'],
        'password': user['login']['password'],
        'email': user['email']
        })
    processed_user.to_csv('/tmp/processed_user.csv', index=None, header=False)


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


