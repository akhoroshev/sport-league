#!/usr/bin/env python3

from flask import Flask
from flask.json import jsonify
from flask import request, abort

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


@app.route('/test', methods=['POST'])
@request_json_fields('address_from', 'address_to')
def test(**options):
    print("address_from: {}".format(options['address_from']))
    print("address_to: {}".format(options['address_to']))

    users = ["ivan", "oleg", "semen"]
    marks = [3, 2, 3] 

    data = {k:v for (k, v) in zip(users, marks)}

    return jsonify(data)
    # return jsonify({'data': [1, 2, 3]})


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5000, debug=True, threaded=False)
