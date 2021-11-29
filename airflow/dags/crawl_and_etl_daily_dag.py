import airflow.utils.dates
from airflow import DAG 
from datetime import datetime, timedelta
from airflow.operators.python_operator import PythonOperator


default_args = {
    'owner': 'longpt',
    'start_date': datetime(2020, 9, 1), 
    'depends_on_past': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
    'catchup': False,
    'email_on_retry': False,
    'email': ['phanthanhlong233@gmail.com'],
    'email_on_failure': True
}

dag = DAG(
    dag_id="daily_crawl_and_etl",
    description="crawl data in stock_name_v2",
    schedule_interval='30 20 * * *',
    start_date=airflow.utils.dates.days_ago(5),
    default_args=default_args,
    max_active_runs=1
)


import tasks.crawl_data as crawl

ticker_crawler = PythonOperator(
    task_id="ticker_crawler",
    python_callable=task.crawl,
    dag=dag)


ticker_ingest = PythonOperator(
    task_id="ticker_push_mongo",
    python_callable=task.test,
    dag=dag)


ticker_crawler >> ticker_ingest




