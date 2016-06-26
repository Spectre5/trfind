import os
from flask import Flask, jsonify, request

from trfind.find import get_all_trip_reports
from trfind.models import Peak

app = Flask(__name__)


@app.route("/find", methods=['POST'])
def find():
    json = request.json

    peak = Peak(**json['data'])
    trip_reports = get_all_trip_reports(peak)
    return jsonify({'data': tuple(trip_report._asdict() for trip_report in trip_reports)})

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
