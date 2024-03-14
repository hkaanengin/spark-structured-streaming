"""
    Generate users from 'Random User API' to populate our data.
"""

import json
import requests

BASE_URL = "https://randomuser.me/api/"

def generate_data(url : str=BASE_URL) -> dict:

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
    person_data = generate_data()