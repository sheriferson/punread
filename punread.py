import json
import os.path
import pickle
import requests

# get the path to punread.py
pathToMe = os.path.realpath(__file__)
pathToMe = os.path.split(pathToMe)[0]

last_updated_path = os.path.join(pathToMe, 'lastupdated.timestamp')
unread_count_path = os.path.join(pathToMe, 'unread.count')
api_token_path = os.path.join(pathToMe, 'api_token')

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

    pickle.dump(last_updated_api, open(last_updated_path, 'wb'))
    pickle.dump(len(unread), open(unread_count_path, 'wb'))
    print(len(unread))
else:
    print(unread_count)
