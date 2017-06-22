import robobrowser
from lxml import etree
from urllib.parse import urljoin, urlencode
from urllib.request import Request, urlopen

import mechanicalsoup
from dateutil.parser import parse as parse_date

from trfind.finders.shared import clean_peak_name
from trfind.html_table import get_basic_data_from_table
from trfind.models import TripReportSummary


CACSADECLIMBERS_SITE = 'Cascade Climbers'

def _cascadeclimbers_data_to_trip_report_summary(cascadeclimbers_data, base_url):
    return TripReportSummary(
        site=CACSADECLIMBERS_SITE,
        link=urljoin(base_url, cascadeclimbers_data['Link']),
        date=parse_date(cascadeclimbers_data['Date'])  if cascadeclimbers_data['Date'] else None,
        title=cascadeclimbers_data['Location|Route'],
        route=None,
        has_gps=None,
        has_photos=None
    )


def find(peak):
    url = 'http://cascadeclimbers.com/forum/ubbthreads.php/ubb/tripreports/'
    post_fields = {
        'ubb': 'tripreports',
        'fromsearch': 1,
        'location': clean_peak_name(peak.name),
        'route': '',
        'user_name': '',
        'forum_id': 0,
        'type_id': 0,
        'photos': 0,
        'buttsubmit': 'Search',
    }

    request = Request(url, urlencode(post_fields).encode())
    result = urlopen(request).read()
    html = etree.HTML(result)

    # CascadeClimbers has an incredible quantity of HTML tables which seem to move around unpredictably.
    # Use the distinctive 'Location|Route' header link to find the right table.
    location_header = html.xpath('.//a[contains(text(),"Location|Route")]')[0]
    results_table = location_header.getparent().getparent().getparent()

    cascadeclimbers_reports = get_basic_data_from_table(results_table, 2)
    reports_in_standardized_format = [
        _cascadeclimbers_data_to_trip_report_summary(report, url)
        for report in cascadeclimbers_reports
    ]

    return reports_in_standardized_format
