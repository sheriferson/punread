import json
import os.path
import pickle
import random
import re
import requests
import sys
import time

# get the path to punread.py
pathToMe = os.path.realpath(__file__)
pathToMe = os.path.split(pathToMe)[0]

last_updated_path = os.path.join(pathToMe, 'lastupdated.timestamp')
unread_count_path = os.path.join(pathToMe, 'unread.count')
links_path = os.path.join(pathToMe, 'links')
api_token_path = os.path.join(pathToMe, 'api_token')
last_run_path = os.path.join(pathToMe, 'lastrun.timestamp')

backup_file = '/Users/sherif/persanalytics/data/unread_pinboard_counts.csv'

def print_random_unread_links(count, unread, n = 30):
    count = str(count) + ' | font=SourceSansPro-Regular color=dodgerblue\n---\n'
    sys.stdout.buffer.write(count.encode('utf-8'))
    random_unread_indexes = random.sample(range(1, len(unread)), 30)
    for ii in random_unread_indexes:
        description = unread[ii]['description']
        description = description.replace("|", "｜")
        link_entry = '📍 ' + description + " | href=" + unread[ii]['href'] + " font=SourceSansPro-Regular color=dodgerblue\n"
        sys.stdout.buffer.write(link_entry.encode('utf-8'))

def log_counts(total_count, unread_count):
   """
   A function to write the time, total bookmark count, and unread bookmark count
   to a csv file.
   """
   now = int(time.time()) 
   row = str(now) + ',' + str(total_count) + ',' + str(unread_count) + '\n'

   with open(backup_file, 'a') as bfile:
       bfile.write(row)

# check if there's a lastrun.timestamp, and if it's there
# check if the script ran less than 5 mins ago
# if yes, quit
if os.path.isfile(last_run_path):
    last_run = pickle.load(open(last_run_path, 'rb'))
    if time.time() - last_run < 300:
        unread_count = pickle.load(open(unread_count_path, 'rb'))
        links = pickle.load(open(links_path, 'rb'))
        unread = [link for link in links if (link['toread'] == 'yes')]
        print_random_unread_links(unread_count, unread)
        exit()
    else:
        pickle.dump(time.time(), open(last_run_path, 'wb'))
else:
    pickle.dump(time.time(), open(last_run_path, 'wb'))

with open(api_token_path, 'rb') as f:
    pintoken = f.read().strip()

par = {'auth_token': pintoken, 'format': 'json'}

if os.path.isfile(last_updated_path) and os.path.isfile(unread_count_path):
    last_updated = pickle.load(open(last_updated_path, 'rb'))
    unread_count = pickle.load(open(unread_count_path, 'rb'))
    links = pickle.load(open(links_path, 'rb'))
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
    pickle.dump(links, open(links_path, 'wb'))

    log_counts(total_count, unread_count)
    print_random_unread_links(unread_count, unread)
else:
    unread = [link for link in links if (link['toread'] == 'yes')]
    print_random_unread_links(unread_count, unread)
