from __future__ import print_function, division, unicode_literals
import numpy as np

from flask import Flask, jsonify, render_template, request
from werkzeug.contrib.cache import SimpleCache
from wtforms import Form, TextField, TextAreaField, SubmitField
cache = SimpleCache()
app = Flask(__name__)

class ContactForm(Form):
	location = TextField("loc")
	date = TextField("dob_day")
	month = TextField("dob_month")
	year = TextField("dob_year")
	submit = SubmitField("Where am I?!")


@app.route('/', methods=["GET", "POST"])
def homepage():
	message = ''
	if request.method == "GET":
		if request.args:
			form = request.args
			print(form["loc"])
			#location = "mycat"
			message = 'So because you were born in '+ form["loc"] +' on '+ form["day"]+'/'+form["month"]+'/'+form["year"]+' you would now be closest to Betelgeuse!'
	return render_template('index.html', message=message)


if __name__ == '__main__':
    app.run(debug=True)