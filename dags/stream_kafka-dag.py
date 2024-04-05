import requests
import json
from datetime import timedelta, datetime
from airflow import DAG
from airflow.operators.python_operator import PythonOperator

BASE_URL = "https://randomuser.me/api/"

def kafka_callback(err, msg):
    if err is not None:
        print(f"Message delivery failed due to {err}")
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}]")


def generate_data(url : str=BASE_URL) -> dict:
    '''
        Creates a dictionary of a random person info which then later be ingested into kafka
    '''
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()['results'][0]
        return {
            "person_id": data['login']['uuid'],
            "name": f"{data['name']['first']} {data['name']['last']}",
            "age": data['dob']['age'],
            "email": data['email'],
            "address": f"{data['location']['street']['name']} {data['location']['street']['number']}",
            "city": data['location']['city'],
            "country": data['location']['country'],
            "longitude": data['location']['coordinates']['longitude'],
            "latitude": data['location']['coordinates']['latitude']
        }

def start_streaming():
    import time
    from confluent_kafka import Producer
    producer = Producer({
                'bootstrap.servers': 'broker-kafka1:9095'
            }
        )
    for _ in range(5):
        person_data = generate_data()
        time.sleep(1)
        producer.produce(
            "people_topic", 
            key = person_data['person_id'], 
            value = json.dumps(person_data), 
            on_delivery = kafka_callback)
        
        print('Produced voter data:{}'.format(person_data))
        producer.flush()
        time.sleep(1)

start_date = datetime(2024, 4, 4)

default_args = {
    'owner': 'airflow',
    'start_date': start_date,
    'retries': 1,
    'retry_delay': timedelta(seconds=5)
}

with DAG(dag_id='generate_random_people', default_args=default_args, schedule_interval='55 10 * * *', catchup=False) as dag:


    data_stream_task = PythonOperator(
    task_id='kafka_data_stream',
    python_callable=start_streaming,
    dag=dag,
    )

    data_stream_task