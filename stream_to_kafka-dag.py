from datetime import timedelta, datetime
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from stream_to_kafka import start_streaming

start_date = datetime(2021, 12, 21, 12, 12)

default_args = {
    'owner': 'airflow',
    'start_date': start_date,
    'retries': 1,
    'retry_delay': timedelta(seconds=5)
}

with DAG(dag_id='random_person_names', default_args=default_args, schedule_interval='0 1 * * *', catchup=False) as dag:


    data_stream_task = PythonOperator(
    task_id='kafka_data_stream',
    python_callable=start_streaming,
    dag=dag,
    )

    data_stream_task