#!/usr/bin/env python

import argparse
import itertools
import traceback

import petl

from .finders import ALL_FINDERS
from .models import Peak, TripReportSummary


def get_all_trip_reports(peak):
    reports = []
    for finder in ALL_FINDERS:
        try:
            reports.extend(finder(peak))
        except Exception as e:
            print('Failed to run {} for {}: {}'.format(finder, peak, traceback.format_exc()))
    return reports


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
        [report._asdict() for report in all_trip_reports],
        header=TripReportSummary._fields
    ).tocsv()
