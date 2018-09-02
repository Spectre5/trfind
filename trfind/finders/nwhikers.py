import json
from datetime import datetime

from bs4 import BeautifulSoup
from dateutil import parser
from functools import partial
from urllib.parse import urljoin, urlencode
from urllib.request import Request, urlopen

from ..models import TripReportSummary


NWHIKERS_SITE = 'NW Hikers'

def _parse_trip_report_row(trip_report_row, relative_to_absolute_url):
    cells = trip_report_row.findAll("td")


    if len(cells) > 5:
        title = cells[2].findAll('a')[0].text.strip()
        date_string = tuple(cells[4].children)[2]
        date = parser.parse(date_string)
        relative_link = cells[2].find('a').attrs['href']

        return TripReportSummary(
            site = NWHIKERS_SITE,
            link = relative_to_absolute_url(relative_link),
            date = date,
            route = '',
            title = title,
            has_gps = False,
            has_photos = False
        )

def _parse_trip_report_rows(trip_report_rows, relative_to_absolute_url):
    return filter(None, (
        _parse_trip_report_row(trip_report_row, relative_to_absolute_url)
        for trip_report_row in trip_report_rows
    ))


def find(peak):
    url = 'http://www.nwhikers.net/forums/search.php'
    post_fields = {
        'search_forum': '3',  # Trip report forum
        'show_results': 'topics',  # Only return titles and metadata
        'and_keywords': '',
        'search_keywords': peak.name,
        'or_keywords': '',
        'not_keywords': '',
        'search_author': '',
        'search_time': '0',
        'search_fields': 'titleonly',  # Only search title
        'return_chars':  '1',
        'sort_by': '0',  # Sort by post time
        'sort_dir': 'DESC',
    }

    request = Request(url, urlencode(post_fields).encode())
    result = urlopen(request).read()
    soup = BeautifulSoup(result, 'lxml')

    trip_report_table = soup.html.body.find('table', {'class' : 'forumline'})
    trip_report_rows = trip_report_table('tr')

    return _parse_trip_report_rows(trip_report_rows, relative_to_absolute_url=partial(urljoin, url))
