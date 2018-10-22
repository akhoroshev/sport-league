#!/usr/bin/env python3

import requests

if __name__ == '__main__':
    res = requests.post('http://127.0.0.1:5000/test',
                        json={'address_from':'bot', 'address_to':'flask'})

    if res.ok:
        print(res.json())
