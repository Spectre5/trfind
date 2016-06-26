import os
from flask import Flask, jsonify, request

from trfind.finders import peakbagger
from trfind.models import Peak

app = Flask(__name__)


@app.route("/find", methods=['POST'])
def find():
    json = request.json

    peak = Peak(**json['data'])
    trip_reports = peakbagger.find(peak)
    return jsonify({'data': trip_reports})

if __name__ == "__main__":
    print 'running'
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
