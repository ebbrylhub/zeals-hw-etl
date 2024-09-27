from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
from scripts.etl_bq_to_gcs import extract_bigquery_bikeshare
from scripts.etl_gcs_to_bq_biglake import create_external_table_bikeshare

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 9, 27),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG('bikeshare_etl', default_args=default_args, schedule_interval='@daily')

def extract_bikeshare():
    extract_bigquery_bikeshare()
    pass

def create_biglake_bikeshare():
    create_external_table_bikeshare()
    pass

extract_task = PythonOperator(
    task_id='extract_bikeshare',
    python_callable=extract_bikeshare,
    dag=dag,
)

biglake_task = PythonOperator(
    task_id='create_biglake_bikeshare',
    python_callable=create_biglake_bikeshare,
    dag=dag,
)

extract_task >> biglake_task
