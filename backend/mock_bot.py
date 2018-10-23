#!/usr/bin/env python3

import requests


def test_request(url='/test',
                 data={'address_from':'bot', 'address_to':'flask'}):
    res = requests.post('http://127.0.0.1:5000' + url, json=data)

    if res.ok:
        print(res.json())
    else:
        print(res)

    print()


if __name__ == '__main__':
    test_request('/register', {'username': 'niikkio', 'password': 'qwerty123'})

    test_request('/event/create', {'username': 'niikkio',
                                   'password': 'qwerty123',
                                   'sport_id': 12,
                                   'timestamp': 1287618,
                                   'location': 'Таймс',
                                   'description': 'Мафия без ограничений',
                                   'participants_number_max': 20,
                                   'status_rating': True})

    test_request('/event/close', {'username': 'niikkio', 
                                  'password': 'qwerty123',
                                  'event_id': 12,
                                  'event_status': 'Canceled',
                                  'results':    {
                                                    'fish': 'W',
                                                    'bird': 'L'
                                                }
                                  })

    test_request('/event/get', {'event_id': 22})

    test_request('/event/list', {'sport_id': 12})

    test_request('/event/join', {'username': 'niikkio', 'password': 'qwerty123', 'event_id': 170})

    test_request('/event/leave', {'username': 'niikkio', 'password': 'qwerty123', 'event_id': 170})

    test_request('/rating/global', {'sport_id': 12})

    test_request('/rating/local', {'sport_id': 4, 'usernames': ['anna', 'oleg']})

    test_request('/sport/list', {})

    test_request('/user/list', {'sport_id': 12})

    test_request('/follow/list', {'username': 'niikkio', 'password': 'qwerty123'})

    test_request('/follow/add', {'username': 'niikkio',
                                 'password': 'qwerty123', 
                                 'sport_id': 12, 
                                 'location': 'Таймс'})

    test_request('/follow/remove', {'username': 'niikkio', 'password': 'qwerty123', 'sport_id': 12})

