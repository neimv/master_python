
import json
from datetime import datetime

import pandas as pd
from pandas import json_normalize
from airflow.models import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.providers.http.sensors.http import HttpSensor
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.hooks.postgres_hook import PostgresHook


def _processing_user(ti):
    users = ti.xcom_pull(task_ids=['extracting_user'])

    if not len(users) or 'results' not in users[0]:
        raise ValueError('User is empty')

    user = users[0]['results'][0]
    processed_user = json_normalize({
        'firstname': user['name']['first'],
        'lastname': user['name']['last'],
        'country': user['location']['country'],
        'username': user['login']['username'],
        'password': user['login']['password'],
        'email': user['email']
    })

    processed_user.to_csv(
        '/tmp/processed_user.csv', index=None
    )


def save_to_pg():
    # pg_hook = PostgresHook.get_hook('db_pg')
    # print(pg_hook)

    df = pd.read_csv('/tmp/processed_user.csv')
    print(df.head())


default_args = {
    'start_date': datetime(2020, 1, 1),
}

with DAG(
    'user_processing',
    schedule_interval='@daily',
    default_args=default_args,
    catchup=False
) as dag:
    # Define task/operators

    creating_table = PostgresOperator(
        task_id='creating_table',
        postgres_conn_id='db_pg',
        sql='''
            CREATE TABLE IF NOT EXISTS users (
                firstname TEXT NOT NULL,
                lastname TEXT NOT NULL,
                country TEXT NOT NULL,
                username TEXT NOT NULL,
                password TEXT NOT NULL,
                email TEXT NOT NULL PRIMARY KEY
            );
        '''
    )

    is_api_available = HttpSensor(
        task_id='is_api_available',
        http_conn_id='user_api',
        endpoint='api/?nat=us,gb'
    )

    extracting_user = SimpleHttpOperator(
        task_id='extracting_user',
        http_conn_id='user_api',
        endpoint='api/?nat=us,gb',
        method='GET',
        response_filter=lambda response: json.loads(response.text),
        log_response=True
    )

    processing_user = PythonOperator(
        task_id='processing_user',
        python_callable=_processing_user
    )

    storing_user = BashOperator(
        task_id='storing_user',
        bash_command='psql postgresql://airflow:airflow@postgres/airflow ' +
                     '''-c "\\copy users FROM '/tmp/processed_user.csv' ''' +
                     '''delimiter ',' csv"'''
    )

    delete_csv = BashOperator(
        task_id='delete_csv',
        bash_command='rm /tmp/processed_user.csv'
    )

    creating_table >> is_api_available >> extracting_user >> \
        processing_user >> storing_user >> delete_csv

# End of file
