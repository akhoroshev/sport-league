#!/usr/bin/env python3

from flask import Flask
from flask.json import jsonify
from flask import request, abort

from datetime import datetime

import sys
sys.path.insert(0, '../facade')

# from mock_adapter import DB
from my_adapter import DB

app = Flask(__name__)


def request_json_fields(*keys):
    def wrapper(func):
        def body(*args, **kwargs):
            try:
                for key in keys:
                    assert key in request.json
                    kwargs.update({key: request.json[key]})
            except AssertionError as err:
                print(err)
                abort(400)
            return func(*args, **kwargs)
        body.__name__ = "wrapped_" + func.__name__
        return body
    return wrapper


def response_error(status, error):
    return jsonify({'status': status, 'error': error})


def response_ok(data={}):
    return jsonify({'status': 0, 'data': data})


@app.route('/register', methods=['POST'])
@request_json_fields('username',
                     'password')
def register(**options):
    status, error = DB.create_user(options['username'],
                                   options['password'])
    if status:
        return response_error(status, error)

    return response_ok()


@app.route('/event/create', methods=['POST'])
@request_json_fields('username', 'password', 'sport_id', 'timestamp', 'location', 'description', 'participants_number_max', 'status_rating')
def create_event(**options):
    user_id, status, error = DB.auth(options['username'], options['password'])
    if status:
        return response_error(status, error)
    
    dt = datetime.utcfromtimestamp(options['timestamp']).strftime('%Y-%m-%d %H:%M:%S')
    event_id, status, error = DB.create_event(user_id,
                                              options['sport_id'],
                                              dt,
                                              options['location'],
                                              options['description'],
                                              options['participants_number_max'],
                                              options['status_rating'])
    if status:
        return response_error(status, error)

    return response_ok({'event_id': event_id})


@app.route('/event/close', methods=['POST'])
@request_json_fields('username', 'password', 'event_id', 'event_status', 'results')
def close_event(**options):
    user_id, status, error = DB.auth(options['username'], options['password'])
    if status:
        return response_error(status, error)

    admin_id, status, error = DB.get_event_admin_id(options['event_id'])
    if status:
        return response_error(status, error)

    if admin_id != user_id:
        return response_error(1, 'you are not event admin')

    participants, status, error = DB.get_event_participants(options['event_id'])
    if status:
        return response_error(status, error)

    if not all(elem in participants for elem in options['results'].keys()):
        return response_error(1, "list of results doesnt match with participants")

    for username, result in options['results'].items():
        points = 2 if result == 'W' else 1 if result == 'D' else 0
        status, errot = DB.set_result(options['event_id'], username, result, points)
        if status:
            return response_error(status, error)

    status, error = DB.update_event_status(options['event_id'], options['event_status'])
    if status:
        return response_error(status, error)

    return response_ok()


@app.route('/event/get', methods=['POST'])
@request_json_fields('event_id')
def get_event(**options):
    event_info, status, error = DB.get_event_info(options['event_id'])
    if status:
        return response_error(status, error)

    # dt = datetime.strptime(event_info['timestamp'], '%Y-%m-%d %H:%M:%S')
    dt = event_info['timestamp']
    event_info['timestamp'] = int(dt.timestamp())

    participants, status, error = DB.get_event_participants(options['event_id'])
    if status:
        return response_error(status, error)

    return response_ok({'event_info': event_info, 'participants': participants})


@app.route('/event/list', methods=['POST'])
@request_json_fields('sport_id')
def get_list_events(**options):
    events, status, error = DB.get_list_events(options['sport_id'])
    if status:
        return response_error(status, error)

    return response_ok({'event_ids': events})


@app.route('/event/join', methods=['POST'])
@request_json_fields('username', 'password', 'event_id')
def join_event(**options):
    user_id, status, error = DB.auth(options['username'], options['password'])
    if status:
        return response_error(status, error)

    participants, status, error = DB.get_event_participants(options['event_id'])
    if status:
        return response_error(status, error)

    event_info, status, error = DB.get_event_info(options['event_id'])
    if status:
        return response_error(status, error)

    if options['username'] in participants:
        return response_error(1, 'you are already registered')

    if len(participants) == event_info['participants_number_max']:
        return response_error(1, 'event is full')

    status, error = DB.join_event(user_id, options['event_id'])
    if status:
        return response_error(status, error)

    return response_ok()


@app.route('/event/leave', methods=['POST'])
@request_json_fields('username', 'password', 'event_id')
def leave_event(**options):
    user_id, status, error = DB.auth(options['username'], options['password'])
    if status:
        return response_error(status, error)

    participants, status, error = DB.get_event_participants(options['event_id'])
    if status:
        return response_error(status, error)

    admin_id, status, error = DB.get_event_admin_id(options['event_id'])
    if status:
        return response_error(status, error)

    if user_id == admin_id:
        return response_error(1, 'admin cant leave event, you should close it')

    if options['username'] not in participants:
        return response_error(1, 'you are not in participants list')

    status, error = DB.leave_event(user_id, options['event_id'])
    if status:
        return response_error(status, error)

    return response_ok()


@app.route('/rating/global', methods=['POST'])
@request_json_fields('sport_id')
def get_global_rating(**options):
    top, status, error = DB.get_top(options['sport_id'], 5)
    if status:
        return response_error(status, error)

    data = {user: points for (user, points) in top}

    return response_ok(data)


@app.route('/rating/local', methods=['POST'])
@request_json_fields('sport_id', 'usernames')
def get_local_rating(**options):
    events, status, error = DB.get_list_events(options['sport_id'])
    if status:
        return response_error(status, error)

    local_events = []

    for event in events:
        participants, status, error = DB.get_event_participants(event)
        if status:
            return response_error(status, error)

        if all(elem in options['usernames'] for elem in participants):
            local_events.append(event)

    result = {username: 0 for username in options['usernames']}

    for event in local_events:
        for username in options['usernames']:
            res, status, error = DB.get_user_result(username, event)
            if status:
                return response_error(status, error)

            if res == 'W':
                result[username] += 2

            if res == 'D':
                result[username] += 1

    return response_ok(result)


@app.route('/sport/list', methods=['POST'])
def get_list_sports(**options):
    sports, status, error = DB.get_list_sports()
    if status:
        return response_error(status, error)

    data = {sport_id: {'name': name, 'description': description} for (sport_id, name, description) in sports}

    return response_ok(data)


@app.route('/user/list', methods=['POST'])
@request_json_fields('sport_id')
def get_list_users(**options):
    users, status, error = DB.get_list_users(options['sport_id'])
    if status:
        return response_error(status, error)

    return response_ok({'usernames': users})


@app.route('/follow/list', methods=['POST'])
@request_json_fields('username', 'password')
def get_list_follows(**options):
    user_id, status, error = DB.auth(options['username'], options['password'])
    if status:
        return response_error(status, error)

    events, status, error = DB.get_list_follows(user_id)
    if status:
        return response_error(status, error)

    return response_ok({'event_ids': events})


@app.route('/follow/add', methods=['POST'])
@request_json_fields('username', 'password', 'sport_id', 'location')
def add_follow(**options):
    user_id, status, error = DB.auth(options['username'], options['password'])
    if status:
        return response_error(status, error)

    status, error = DB.add_follow(user_id, options['sport_id'], options['location'])
    if status:
        return response_error(status, error)

    return response_ok()


@app.route('/follow/remove', methods=['POST'])
@request_json_fields('username', 'password', 'sport_id')
def remove_follow(**options):
    user_id, status, error = DB.auth(options['username'], options['password'])
    if status:
        return response_error(status, error)

    status, error = DB.remove_follows(user_id, options['sport_id'])
    if status:
        return response_error(status, error)

    return response_ok()


@app.route('/location/list', methods=['POST'])
def get_list_locations(**options):
    locations, status, error = DB.get_list_locations()
    if status:
        return response_error(status, error)

    data = {location_id: {'name': name, 'description': description} for (location_id, name, description, _, _) in locations}

    return response_ok(data)


@app.route('/event/user', methods=['POST'])
@request_json_fields('username')
def get_user_events(**options):
    events, status, error = DB.get_user_events(options['username'])
    if status:
        return response_error(status, error)

    return response_ok({'event_ids': events})


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True, threaded=False)
