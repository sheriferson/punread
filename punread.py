import json
import os.path
import pickle
import requests
import time

# get the path to punread.py
pathToMe = os.path.realpath(__file__)
pathToMe = os.path.split(pathToMe)[0]

last_updated_path = os.path.join(pathToMe, 'lastupdated.timestamp')
unread_count_path = os.path.join(pathToMe, 'unread.count')
api_token_path = os.path.join(pathToMe, 'api_token')

backup_file = '/Users/sherif/persanalytics/data/unread_pinboard_counts.csv'

def log_counts(total_count, unread_count):
   """
   A function to write the time, total bookmark count, and unread bookmark count
   to a csv file.
   """
   now = int(time.time()) 
   row = str(now) + ',' + str(total_count) + ',' + str(unread_count) + '\n'

   with open(backup_file, 'a') as bfile:
       bfile.write(row)

with open(api_token_path, 'rb') as f:
    pintoken = f.read().strip()

par = {'auth_token': pintoken, 'format': 'json'}

if os.path.isfile(last_updated_path) and os.path.isfile(unread_count_path):
    last_updated = pickle.load(open(last_updated_path, 'rb'))
    unread_count = pickle.load(open(unread_count_path, 'rb'))
else:
    last_updated = ''
    unread_count = 0

last_updated_api_request = requests.get('https://api.pinboard.in/v1/posts/update',
        params = par)

last_updated_api = last_updated_api_request.json()['update_time']

if last_updated != last_updated_api:
    r = requests.get('https://api.pinboard.in/v1/posts/all',
            params = par)

    links = json.loads(r.text)

    unread = [link for link in links if (link['toread'] == 'yes')]
    total_count = len(links)
    unread_count = len(unread)

    pickle.dump(last_updated_api, open(last_updated_path, 'wb'))
    pickle.dump(unread_count, open(unread_count_path, 'wb'))

    log_counts(total_count, unread_count)
    print(unread_count)
else:
    print(unread_count)
