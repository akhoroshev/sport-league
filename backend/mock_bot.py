#!/usr/bin/env python3

import requests


def test_request(url, data):
    res = requests.post('http://172.18.0.1:5000' + url, json=data)

    if res.ok:
        print(res.json())
    else:
        print(res)

    print()


if __name__ == '__main__':
    # test_request('/register', {'username': 'bobbys', 'password': '678rexrex678'})

    # test_request('/follow/add', {'username': 'bobbys', 'password': '678rexrex678', 'sport_id':1, 'location':2})
    # test_request('/follow/add', {'username': 'bobbys', 'password': '678rexrex678', 'sport_id':2, 'location':3})
    # test_request('/follow/add', {'username': 'niikkio', 'password': 'qwerty7103', 'sport_id':2, 'location':3})

    # test_request('/follow/get', {'username': 'bobbys', 'password': '678rexrex678', 'follow_id':2})
    # test_request('/follow/get', {'username': 'niikkio', 'password': 'qwerty7103', 'follow_id':3})
    
    # test_request('/follow/list', {'username': 'bobbys', 'password': '678rexrex678'})

    test_request('/follow/remove', {'username': 'niikkio', 'password': 'qwerty7103', 'follow_id': 2})
    test_request('/follow/remove', {'username': 'niikkio', 'password': 'qwerty7103', 'follow_id': 3})
