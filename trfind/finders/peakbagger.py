import json
import urllib
import pkg_resources
from datetime import datetime

from bs4 import BeautifulSoup
from dateutil import parser
from functools import partial
from urllib.parse import urljoin

from ..models import TripReportSummary


PEAKBAGGER_SITE = 'Peakbagger'

def _parse_date(date_string):
    try:
        return parser.parse(date_string, default=datetime(2000, 1, 1))
    except (ValueError, AttributeError):
        return None

def _get_href(cell):
    return cell.a['href'] if cell.a else None

def _has_gps(cell):
    return True if cell.text.strip() == 'GPS' else False

def _parse_trip_report_row(trip_report_row, relative_to_absolute_url):
    cells = trip_report_row.findAll("td")

    if len(cells) >= 5:
        link =  relative_to_absolute_url(_get_href(cells[0]))
        if link:
            raw_route = cells[4].text.strip()
            route = None if raw_route == '&nbsp;' else raw_route
            return TripReportSummary(
                site = PEAKBAGGER_SITE,
                link = link,
                date = _parse_date(cells[0].text.strip()),
                route = route,
                title = None,
                has_gps = _has_gps(cells[2]),
                has_photos = False
            )

def _parse_trip_report_rows(trip_report_rows, relative_to_absolute_url):
    return filter(None, (
        _parse_trip_report_row(trip_report_row, relative_to_absolute_url)
        for trip_report_row in trip_report_rows
    ))


def _convert_peak_to_pid(peak):
    peakbagger_id_lookup = json.loads(pkg_resources.resource_string('trfind.finders', 'peakbagger_id_lookup.json').decode('utf8'))
    fuzzy_match_deltas = [0, -0.001, 0.001]
    for lat_delta in fuzzy_match_deltas:
        for lon_delta in fuzzy_match_deltas:
            lat_lon_string = '{lat:.3f}, {lon:.3f}'.format(
                lat=peak.lat + lat_delta,
                lon=peak.lon + lon_delta
            )
            peak_id = peakbagger_id_lookup.get(lat_lon_string)
            if peak_id is not None:
                return peak_id
    return None


def find(peak):
    peakbagger_peak_id = _convert_peak_to_pid(peak)
    if peakbagger_peak_id is None:
        return []

    url = 'http://www.peakbagger.com/climber/PeakAscents.aspx?pid={}&sort=AscentDate&u=ft&y=9999'.format(peakbagger_peak_id)
    page = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(page, 'lxml')

    trip_report_table = soup.html.body.find('table', {'class': 'gray'})
    trip_report_rows = trip_report_table('tr')

    return _parse_trip_report_rows(trip_report_rows, relative_to_absolute_url=partial(urljoin, url))
