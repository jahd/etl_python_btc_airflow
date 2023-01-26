from datetime import timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from datetime import datetime
from btc_etl import run_btc_etl
import os


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 26, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=1)
}

dag = DAG(
    'btc_dag',
    default_args=default_args,
    description='Our btc dag',
    schedule_interval=timedelta(months=1),
)

run_etl = PythonOperator(
    task_id='whole_btc_etl',
    python_callable=run_btc_etl,
    dag=dag,
)
