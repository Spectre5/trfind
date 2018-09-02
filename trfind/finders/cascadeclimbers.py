
import requests
from urllib.parse import urljoin
from dateutil.parser import parse as parse_date
from bs4 import BeautifulSoup

from ..finders.shared import clean_peak_name
from ..models import TripReportSummary

CACSADECLIMBERS_SITE = 'Cascade Climbers'


def _cascadeclimbers_data_to_trip_report_summary(cascadeclimbers_data, base_url):
    soup = BeautifulSoup(cascadeclimbers_data['TR_ROUTE'], 'lxml').find('a')
    link = soup['href']
    route_title = soup.string
    return TripReportSummary(
        site=CACSADECLIMBERS_SITE,
        link=urljoin(base_url, link),
        date=parse_date(cascadeclimbers_data['TR_POSTED']),
        title=cascadeclimbers_data['TR_LOCATION'],
        route=route_title,
        has_gps=None,
        has_photos=None
    )


def find(peak):
    url = 'https://cascadeclimbers.com/forum/applications/tripreport/interface/TripReportAPI/tr_ajax.php'
    post_fields = {
        'columns[0][data]': 'TR_POSTED',
        'columns[0][searchable]': 'true',
        'columns[0][search][value]': '',
        'columns[1][data]': 'TYPE_NAME',
        'columns[1][searchable]': 'true',
        'columns[1][search][value]': '',
        'columns[2][data]': 'TR_LOCATION',
        'columns[2][searchable]': 'true',
        'columns[2][search][value]': '',
        'columns[3][data]': 'TR_ROUTE',
        'columns[3][searchable]': 'true',
        'columns[3][search][value]': '',
        'columns[4][data]': 'FORUM_NAME',
        'columns[4][searchable]': 'true',
        'columns[4][search][value]': '',
        'columns[5][data]': 'name',
        'columns[5][searchable]': 'true',
        'columns[5][search][value]': '',
        'search[value]': clean_peak_name(peak.name),
    }

    results = requests.get(url, params=post_fields)

    reports_in_standardized_format = [
        _cascadeclimbers_data_to_trip_report_summary(report, url)
        for report in results.json()['data']
    ]

    return reports_in_standardized_format
