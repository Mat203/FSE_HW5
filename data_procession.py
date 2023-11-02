import requests
import time
import json
from datetime import datetime

user_data = []

def get_data(offset):
    url = f"https://sef.podkolzin.consulting/api/users/lastSeen?offset={offset}"
    response = requests.get(url)
    data = response.json()
    return data['data']

def update_user_data(user, previous_state):
    user_id = user['userId']
    previous_user = previous_state.get(user_id, {})
    previous_user.update(user)
    previous_state[user_id] = previous_user
    return previous_user

previous_state = {}

def save_user_data_to_json(data):
    with open('user_data.json', 'w') as json_file:
        json.dump(data, json_file, indent=4)

def print_json_file(filename):
    with open(filename, 'r') as json_file:
        data = json.load(json_file)
        print(json.dumps(data, indent=4))

def fetch_and_update_data():
    offset = 0
    counter = 0

    while True:
        data = get_data(offset)

        if not data or counter > 1000:
            break

        for d in data:
            user_id = d['userId']
            if user_id not in previous_state:
                first_detection_time = datetime.now().isoformat()
            else:
                first_detection_time = previous_state[user_id].get('firstDetectionTime', None)

            user = {
                'userId': user_id,
                'isOnline': d['isOnline'],
                'lastSeenDate': d['lastSeenDate'],
                'nickname': d['nickname'],
                'lastName': d['lastName'],
                'registrationDate': d['registrationDate'],
                'firstDetectionTime': first_detection_time,
            }
            updated_user = update_user_data(user, previous_state)

            if updated_user['userId'] not in [user['userId'] for user in user_data]:
                user_data.append(updated_user)
                save_user_data_to_json(user_data)
            

        offset += len(data)
        counter += 1

if __name__ == "__main__":
    while True:
        fetch_and_update_data()
        print("User Data JSON:")
        print_json_file('user_data.json')
        time.sleep(10)
