import requests
import json
import time
from datetime import datetime
from dateutil.parser import parse

def get_data(offset):
    url = f"https://sef.podkolzin.consulting/api/users/lastSeen?offset={offset}"
    response = requests.get(url)
    data = response.json()
    return data['data']

def update_user_data(user, previous_state):
    if user['isOnline']:
        if user['userId'] not in previous_state or not previous_state[user['userId']]['isOnline']:
            user['onlinePeriods'] = previous_state.get(user['userId'], {}).get('onlinePeriods', [])
            user['onlinePeriods'].append([datetime.now().isoformat(), None])
        else:
            user['onlinePeriods'] = previous_state[user['userId']]['onlinePeriods']
    else:
        if user['userId'] in previous_state and previous_state[user['userId']]['isOnline']:
            last_online_period = previous_state[user['userId']]['onlinePeriods'][-1]
            last_online_period[1] = datetime.now().isoformat()
            user['onlinePeriods'] = previous_state[user['userId']]['onlinePeriods']
        else:
            user['onlinePeriods'] = previous_state.get(user['userId'], {}).get('onlinePeriods', [])
    return user

previous_state = {} 
deleted_users = set()

def fetch_and_update_data():
    offset = 0
    all_data = []
    counter = 0

    while True:
        data = get_data(offset)

        if not data or counter > 1000: 
            break
        
        for d in data:
            if d['userId'] in deleted_users:
                continue
            user = { 'userId': d['userId'], 'isOnline': d['isOnline'], 'lastSeenDate': d['lastSeenDate'] }
            updated_user = update_user_data(user, previous_state)
            user['totalSecondsOnline'] = calculate_online_time(user)

            if updated_user['userId'] not in [user['userId'] for user in all_data]:
                all_data.append(updated_user)

            previous_state[updated_user['userId']] = updated_user

        offset += len(data)
        counter += 1


    with open('all_data.json', 'w') as f:
        json.dump(all_data, f)

def calculate_online_time(user):
    total_seconds_online = 0
    for period in user['onlinePeriods']:
        start_time = parse(period[0])
        end_time = parse(period[1]) if period[1] else datetime.now()
        total_seconds_online += (end_time - start_time).total_seconds()
    return total_seconds_online

def calculate_days(user):
    periods = user['onlinePeriods']
    if not periods:
        return 0
    start_date = parse(periods[0][0]).date()
    end_date = parse(periods[-1][-1]).date() if periods[-1][-1] else start_date
    return (end_date - start_date).days + 1

def calculate_average_times(user):
    days = calculate_days(user)
    if days == 0:
        return 0, 0
    total_seconds_online = calculate_online_time(user)
    daily_average = total_seconds_online / days
    weekly_average = daily_average * 7
    return weekly_average, daily_average

def delete_user_data(user_id):
    with open('all_data.json', 'r') as f:
        all_data = json.load(f)
    all_data = [user for user in all_data if user['userId'] != user_id]
    with open('all_data.json', 'w') as f:
        json.dump(all_data, f)
    deleted_users.add(user_id)
    if user_id in previous_state:
        del previous_state[user_id]

def calculate_min_max(user):
    daily_times = []
    for period in user['onlinePeriods']:
        start_time = parse(period[0])
        end_time = parse(period[1]) if period[1] else datetime.now()
        daily_times.append((end_time - start_time).total_seconds())
    return min(daily_times), max(daily_times)

def generate_report(report_name, metrics, users):
    with open('all_data.json', 'r') as f:
        all_data = json.load(f)
    
    report_data = {}
    for user in all_data:
        if user['userId'] not in users:
            continue
        user_report = {}
        if 'dailyAverage' in metrics:
            _, daily_average = calculate_average_times(user)
            user_report['dailyAverage'] = daily_average
        if 'weeklyAverage' in metrics:
            weekly_average, _ = calculate_average_times(user)
            user_report['weeklyAverage'] = weekly_average
        if 'total' in metrics:
            user_report['total'] = calculate_online_time(user)
        if 'min' in metrics or 'max' in metrics:
            min_time, max_time = calculate_min_max(user)
            if 'min' in metrics:
                user_report['min'] = min_time
            if 'max' in metrics:
                user_report['max'] = max_time
        report_data[user['userId']] = user_report

    
    with open(f'{report_name}.json', 'w') as f:
        json.dump(report_data, f)

    print("Report successfully created.")

if __name__ == "__main__":
    while True:
        fetch_and_update_data()
        time.sleep(10)