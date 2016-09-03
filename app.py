import os

from flask import Flask, jsonify, request
from flask_cors import cross_origin

from trfind.find import get_all_trip_reports
from trfind.models import Peak
from trfind.weather import get_weather

app = Flask(__name__)


def _get_peak_from_request():
    json = request.json or json.loads(request.data)
    return Peak(**json['data'])


@app.route('/find', methods=['POST'])
@cross_origin('http://www.climbplan.com', 'localhost')
def find():
    peak = _get_peak_from_request()
    trip_reports = get_all_trip_reports(peak)

    return jsonify({'data': tuple(trip_report._asdict() for trip_report in trip_reports)})


@app.route('/weather', methods=['POST'])
@cross_origin('http://www.climbplan.com', 'localhost')
def weather():
    peak = _get_peak_from_request()
    weathers = get_weather(peak)

    return jsonify({'data': tuple(weather._asdict() for weather in weathers)})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
