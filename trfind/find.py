import argparse
import itertools
import sys

import petl

from trfind.finders import ALL_FINDERS
from trfind.models import Peak, TripReportSummary


def get_all_trip_reports(peak):
    return list(itertools.chain(
        *[finder(peak) for finder in ALL_FINDERS]
    ))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('lat', type=float)
    parser.add_argument('lon', type=float)
    parser.add_argument(
        'name',
        nargs='+',
        action='append',
        help='Peak name to search for - multiple words will form one search term'
    )
    args = parser.parse_args()
    peak_name = ' '.join(*args.name) or 'Mount Stuart'

    peak = Peak(peak_name, args.lat, args.lon)
    print('Finding trip reports for', peak)

    all_trip_reports = get_all_trip_reports(peak)

    petl.fromdicts(
        [report.__dict__ for report in all_trip_reports],
        header=TripReportSummary._fields
    ).tocsv()
