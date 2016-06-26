from datetime import datetime
from functools import partial
from urlparse import urljoin

from BeautifulSoup import BeautifulSoup
import mechanize

from trfind.models import TripReportSummary


PEAKBAGGER_SITE = 'Peakbagger'

def _parse_date(date_string):
    try:
        return parser.parse(date_string, default=datetime(2000, 1, 1))
    except Exception:
        return None

def _get_href(cell):
    return cell.a['href'] if cell.a else None

def _parse_trip_report_row(trip_report_row, relative_to_absolute_url):
    cells = trip_report_row.findAll("td")

    if len(cells) >= 5:
        link =  relative_to_absolute_url(_get_href(cells[0]))
        if link:
            return TripReportSummary(
                site = PEAKBAGGER_SITE,
                link = link,
                date = _parse_date(cells[0].text.strip()),
                route = cells[4].text.strip(),
                title = None,
                has_gps = cells[2].text.strip(),
                has_photos = False
            )

def _parse_trip_report_rows(trip_report_rows, relative_to_absolute_url):
    return filter(None, (
        _parse_trip_report_row(trip_report_row, relative_to_absolute_url)
        for trip_report_row in trip_report_rows
    ))

def _convert_peak_to_pid(peak):
    return 2182


def find(peak):
    br = mechanize.Browser()
    peakbagger_peak_id = _convert_peak_to_pid(peak)
    url = 'http://www.peakbagger.com/climber/PeakAscents.aspx?pid={}&sort=AscentDate&u=ft&y=9999'.format(peakbagger_peak_id)
    page = br.open(url)
    html = page.read()
    soup = BeautifulSoup(html)

    trip_report_table = soup.html.body.findAll('table')[2].findAll('table')[2]
    trip_report_rows = trip_report_table('tr')

    return _parse_trip_report_rows(trip_report_rows, relative_to_absolute_url=partial(urljoin, page.geturl()))
