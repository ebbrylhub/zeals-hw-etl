from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
from scripts.extract_data import extract_bigquery_data
from scripts.biglake_create import create_external_table

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 9, 27),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG('bikeshare_etl', default_args=default_args, schedule_interval='@daily')

def extract_data():
    extract_bigquery_data()
    pass

def create_biglake_table():
    create_external_table()
    pass

extract_task = PythonOperator(
    task_id='extract_data',
    python_callable=extract_data,
    dag=dag,
)

biglake_task = PythonOperator(
    task_id='create_biglake_table',
    python_callable=create_biglake_table,
    dag=dag,
)

extract_task >> biglake_task
