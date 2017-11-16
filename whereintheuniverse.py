from __future__ import print_function, division, unicode_literals
import numpy as np

from flask import Flask, jsonify, render_template, request
from werkzeug.contrib.cache import SimpleCache
cache = SimpleCache()
app = Flask(__name__)

@app.route('/')
def homepage():
	return render_template('index.html')

@app.route('/', methods=["GET", "POST"])
def hello_world():
	location = request.form('loc')
	print("hello")
	print(location)
	return location



if __name__ == '__main__':
    app.run()