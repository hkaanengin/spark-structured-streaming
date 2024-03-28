"""
    Generate users from 'Random User API' to populate our data.
"""

import time
import requests
import json
from confluent_kafka import Producer, SerializingProducer

BASE_URL = "https://randomuser.me/api/"

def kafka_callback(err, msg):
    if err is not None:
        print(f"Message delivery failed due to {err}")
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}]")


def generate_data(url : str=BASE_URL) -> dict:
    '''
        Creates a dictionary of a random person info which then later be produced into kafka
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

if __name__ == '__main__':
    producer = SerializingProducer({
                'bootstrap.servers': 'localhost:29095'
            }
        )
    for _ in range(5):
        person_data = generate_data()
        print("trying to produce!!!------")
        time.sleep(1)
        producer.produce(
            "people_topic", 
            key = person_data['person_id'], 
            value = json.dumps(person_data), 
            on_delivery = kafka_callback)
        
        print('Produced voter data:{}'.format(person_data))
        time.sleep(1)