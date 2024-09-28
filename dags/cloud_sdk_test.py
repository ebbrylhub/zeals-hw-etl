from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 9, 28),
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

dag = DAG('cloud-sdk-test', default_args=default_args, schedule_interval='@once')

sdk_test_task = BashOperator(
    task_id = 'bigquery-test',
    bash_command = """bq query --use_legacy_sql=False "SELECT COUNT(*) FROM bigquery-public-data.austin_bikeshare.bikeshare_trips"
    """,
    dag=dag
)

sdk_test_task