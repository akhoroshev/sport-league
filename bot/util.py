import requests
import json
import datetime
import time


host_name = 'http://backend:5000'


def post(url, args={}, auth=None):
    if auth:
        args.update(auth)
    headers = {'content-type': 'application/json'}
    response = requests.post(
        host_name+url,
        data=json.dumps(args),
        headers=headers,
        timeout=5
    )
    try:
        result = response.json()
    except Exception:
        raise Exception(str(response) + response.text)
    if 'error' in result:
        raise Exception(result['error'])
    return result['data']


def sport_list():
    data = post('/sport/list')
    return [data[x]['name'] for x in data]


def id_to_sport(id):
    data = post('/sport/list')
    if id in data:
        return data[id]['name']
    return None


def parse_sport_id(sport_name):
    data = post('/sport/list')
    res = [x for x in data if data[x]['name'] == sport_name]
    if res:
        return res[0]
    raise ValueError('Выбери вид спорта еще раз')


def id_to_location(id):
    data = post('/location/list')
    if id in data:
        return data[id]['name']
    return None


def location_list():
    data = post('/location/list')
    return [data[x]['name'] for x in data]


def parse_location_id(location_name):
    data = post('/location/list')
    res = [x for x in data if data[x]['name'] == location_name]
    if res:
        return res[0]
    raise ValueError('Выбери локацию еще раз')


def timestamp_to_human(ts):
    return time.ctime(ts)


def time_list():
    return ['Сейчас', 'Через пару часов', 'Вечером']


def parse_time(msg_time):
    cur_time = int(time.time())
    action = {
        'Сейчас': lambda : cur_time,
        'Через пару часов': lambda : cur_time + 2 * 60 * 60,
        'Вечером': lambda : cur_time - (cur_time % 86400) + 72000
    }
    if msg_time in action:
        return action[msg_time]()
    try:
        ans = datetime.datetime.strptime(msg_time, "%m-%d-%H").replace(year=datetime.date.today().year)
        if ans < datetime.datetime.today():
            ans = ans.replace(year=ans.year + 1)
        return int(time.mktime(ans.timetuple()))
    except Exception as e:
        raise ValueError('Выбери время еще раз')


def parse_ranked(msg_ranked):
    if msg_ranked == 'Да':
        return True
    elif msg_ranked == 'Нет':
        return False
    else:
        raise ValueError('Ответь Да/Нет')
