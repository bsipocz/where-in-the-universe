from __future__ import print_function, division, unicode_literals
from flask import Flask, jsonify, render_template, request
from werkzeug.contrib.cache import SimpleCache
cache = SimpleCache()
app = Flask(__name__)


@app.route('/', methods=["GET", "POST"])
def homepage():
	message = ''
	if request.method == "GET":
		if request.args:
			form = request.args
			message = 'So because you were born in '+ form["loc"] +' on '+ form["day"]+'/'+form["month"]+'/'+form["year"]+' you would now be closest to Betelgeuse!'
	return render_template('index.html', message=message)


if __name__ == '__main__':
    app.run(debug=True)