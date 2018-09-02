#!/usr/bin/env python

import os

from flask import Flask, jsonify, request, abort
from flask_cors import cross_origin

from trfind.find import get_all_trip_reports
from trfind.models import Peak
from trfind.weather import get_weather

app = Flask(__name__)


def _get_peak_from_request_or_400():
    try:
        # *TESTING* - comment out this line and @app.route below and visit:
        # localhost:5000/find
        # return Peak(lat=48.51152, lon=-121.05789, name="Forbidden Peak")

        return Peak(**request.json['data'])
    except TypeError:
        abort(400)

# *TESTING* - Include 'GET' in the methods
# @app.route('/find', methods=['POST', 'GET'])
@app.route('/find', methods=['POST'])
@cross_origin('http://www.climbplan.com', 'localhost')
def find():
    peak = _get_peak_from_request_or_400()
    trip_reports = get_all_trip_reports(peak)

    return jsonify({'data': tuple(trip_report._asdict() for trip_report in trip_reports)})


@app.route('/weather', methods=['POST'])
@cross_origin('http://www.climbplan.com', 'localhost')
def weather():
    peak = _get_peak_from_request_or_400()
    weathers = get_weather(peak)

    return jsonify({'data': tuple(weather._asdict() for weather in weathers)})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
