import requests
import time
from datetime import datetime, timedelta

def line_notify(message):
    url = 'https://notify-api.line.me/api/notify'
    headers = {'Authorization': 'Bearer pT1euenXWTM7xS5Os2EqhnumXmYwtF1tpJHivQKGdzr'}
    payload = {'message': message}
    r = requests.post(url, headers=headers, data=payload)
    return message

def format_date(unix_timestamp):
    dt = datetime.utcfromtimestamp(int(unix_timestamp))
    dt_utc7 = dt + timedelta(hours=7)
    formatted_timestamp = dt_utc7.strftime("%Y-%m-%d %H:%M UTC+7")
    return formatted_timestamp

def list_pop():
    global existing_ids
    existing_ids.pop(0)

def notify_notice(id, date, title):
    url = "https://citizen.dosi.world/support/notice/"+str(id)
    date = format_date(date)
    print(line_notify(title+"\n"+date+"\n"+url))

def add_id(id):
    global existing_ids
    existing_ids.append(id)

def check_notice(url):
    print("Checking for new notice")
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json().get('result').get('documents')
        
        current_ids = []
        for d in data:
            current_ids.append(d['id'])

        new_ids = [item for item in current_ids if item not in existing_ids]

        if len(new_ids)>0:
            for id in new_ids:
                add_id(id)
                notice = [item for item in data if item['id'] == id]
                notify_notice(id, str(notice[0]['registered'])[:10], notice[0]['title'])
        else:
            print("No new notice")

def initiate_ids(url):
    response = requests.get(url).json().get('result').get('documents')
    ids = []
    for d in response:
        ids.append(d['id'])
    print(ids)
    return ids

###########################################
list_url = 'https://citizen.dosi.world/lan/api/v1/DOSI_Citizen/web/document/notice?lang=en&size=100'

# initiate the notice list already seen
existing_ids = initiate_ids(list_url)
list_pop()

# Continuously check for new blog entries
while True:
    time.sleep(60)
    check_notice(list_url)