from airflow.models import DAG
from airflow.providers.sqlite.operators.sqlite import SqliteOperator
from datetime import datetime

default_args = {
    'start_date': datetime(2020, 1, 1)
}

with DAG('user_processing', schedule_interval='@daily', default_args=default_args, catchup=False) as dag:
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