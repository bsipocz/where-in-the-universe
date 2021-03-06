from __future__ import print_function, division, unicode_literals

import numpy as np

from astropy.coordinates import EarthLocation, AltAz, ICRS, SkyCoord
from astropy.time import Time
import astropy.units as u
from astroquery.simbad import Simbad
from astropy.table import Table

from flask import Flask, jsonify, render_template, request
from werkzeug.contrib.cache import SimpleCache
cache = SimpleCache()
app = Flask(__name__)


simbad = Simbad()
simbad.add_votable_fields('parallax')
all_100lyr = simbad.query_criteria('plx>32')
all_100lyr['distance_lyr'] = all_100lyr['PLX_VALUE'].to(u.lightyear, equivalencies=u.parallax())

all_100lyr_coord = SkyCoord(
    all_100lyr['RA'], all_100lyr['DEC'], unit=(u.hourangle, u.degree),
    distance=all_100lyr['distance_lyr'])


def zenith_at_birth(address, time):

    # If the query returns more than one location (e.g., searching on
    # address='springfield'), this function will use the first returned
    # location. 'address' can be a full specified address though.
    location = EarthLocation.of_address(address)

    birth_time = Time(time)
    age = (Time.now() - birth_time).to(u.year)

    zenith = AltAz(obstime=birth_time, location=location, alt=90*u.deg,
                   az=0*u.deg)

    zenith_icrs = zenith.transform_to(ICRS)

    return zenith_icrs, age


def find_closest_object(coord, age):
    now_coordinate = SkyCoord(coord, distance=age.value*u.lightyear)
    separations = now_coordinate.separation_3d(all_100lyr_coord)
    closest_ind = np.argmin(separations)

    closest= {'name': all_100lyr['MAIN_ID'][closest_ind],
              'distance': all_100lyr['distance_lyr'][closest_ind],
              'separation': separations[closest_ind]}
        
    return closest


@app.route('/', methods=["GET", "POST"])
def homepage():
    message = ''
    return render_template('index.html', message=message)

@app.route('/formuser', methods=["GET"])
def formpage():
	message=''
	if request.method == "GET":
		if request.args:
			form = request.args
			time = form["year"]+'-'+form["month"]+'-'+form["day"]+" "+form["time_hour"]+":"+form["time_minutes"]
			location = form["loc"]
			zenith, age = zenith_at_birth(location, time)
			closest = find_closest_object(zenith, age)
			message = ('If you were launched from Earth at light speed from '+ form["loc"] +' on '
                       + form["day"]+'/'+form["month"]+'/'+form["year"]+' at '+form['time_hour']+':'+form["time_minutes"]+
                       ', you would now be closest to the star {} which would be {:.2f} '
                       'light years away from you and {:.2f} light years from '
                       'Earth! Turns out space is really empty.'.format(closest['name'].decode("utf-8"), closest['separation'], closest['distance']))
	return message

if __name__ == '__main__':
    app.run(debug=True)
