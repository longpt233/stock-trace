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
    dag_id="daily_crawl_com_name_v2",
    description="crawl all price of stock in stock_name_v2",
    schedule_interval='30 20 * * *',      # crawl luc 8 30 toi 
    start_date=airflow.utils.dates.days_ago(5),
    default_args=default_args,
    max_active_runs=1
)


import tasks.crawl_utils.crawler as crawl

ticker_crawler_all = PythonOperator(
    task_id="ticker_crawler_all",
    python_callable=crawl.crawl_all_company(),
    dag=dag)

ticker_crawler = PythonOperator(
    task_id="ticker_crawler_",
    python_callable=task.crawl,
    dag=dag)


ticker_crawler_all >> ticker_crawler




