#!/usr/bin/python3
# -*- coding: utf-8 -*-


import time
from flask import Flask


app = Flask(__name__)


@app.route('/<int:x>')
def index(x):
    time.sleep(x)
    return "%s It works" % x


@app.route('/error')
def error():
    time.sleep(3)
    return "error!"

if __name__ == '__main__':
    app.run(debug=True)
