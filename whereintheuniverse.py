#################################################################
### This python file is a flask app to take a date, time and location and calculate
### the zenith at that time and find where the nearest objects are to you if you were
### launched from there at the speed of light. Hosted on heroku. 
##################################################################

from __future__ import print_function, division, unicode_literals
import numpy as np

from flask import Flask, jsonify, render_template, request
from werkzeug.contrib.cache import SimpleCache
cache = SimpleCache()
app = Flask(__name__)

@app.route('/')
def homepage():
	return render_template('index.html')

@app.route('/locations/<loc>/', methods=["GET", "POST"])
def hello_world(loc):
	return loc



if __name__ == '__main__':
    app.run()