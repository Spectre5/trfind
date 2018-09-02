import urllib
from urllib.parse import urljoin, urlencode
import requests
from bs4 import BeautifulSoup

from dateutil.parser import parse as parse_date
from lxml import etree

from ..finders.shared import clean_peak_name
from ..models import TripReportSummary

SUMMITPOST_SITE = 'SummitPost'


def _summitpost_data_to_trip_report_summary(summitpost_data, base_url):
    return TripReportSummary(
        site=SUMMITPOST_SITE,
        link=urljoin(base_url, summitpost_data['Link']),
        date=parse_date(summitpost_data['Climb_Date']),
        title=summitpost_data['Title'],
        route=None,
        has_gps=None,
        has_photos=None
    )


def _summitpost_results_div_to_dict(soup):
    results = []

    for div in soup.find_all('div', {'class': 'custom-card-item'}):
        trip_report = {}
        for tag in div.select("div.cci-details b"):
            if 'Date Climbed/Hiked' in tag.text:
                trip_report['Climb_Date'] = tag.next_sibling.strip()

        a = div.select("p.cci-title a")[0]
        trip_report['Title'] = a.text
        trip_report['Link'] = a['href']

        results.append(trip_report)

    return results


def _summitpost_url_format(peak_name):
    query_string = urlencode({'object_name_5': peak_name})
    return (
        'http://www.summitpost.org/object_list.php?object_type=5&{}'
        .format(query_string)
    )


def find(peak):
    response = requests.get(_summitpost_url_format(
        peak_name=clean_peak_name(peak.name)
    ))

    results = BeautifulSoup(response.text, 'lxml')

    summitpost_reports = _summitpost_results_div_to_dict(results)
    base_url = response.url
    reports_in_standardized_format = [
        _summitpost_data_to_trip_report_summary(report, base_url)
        for report in summitpost_reports
    ]

    return reports_in_standardized_format
