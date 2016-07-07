from urlparse import urljoin

from dateutil.parser import parse as parse_date
from lxml import etree
import mechanize
import petl

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


def _clean_name_for_cascadeclimbers(name):
    ''' CascadeClimbers' search is awful.
    If you search for 'Mount Stuart' you will get results for all 'Mounts'.
    Put name in quotes for better results.
    '''
    return '"{}"'.format(name)


def find(peak):
    browser = mechanize.Browser()
    browser.open('http://cascadeclimbers.com/forum/ubbthreads.php/ubb/tripreports')

    browser.select_form(nr=1)
    browser['location'] = _clean_name_for_cascadeclimbers(peak.name)

    results_response = browser.submit()
    html = etree.HTML(results_response.read())

    # CascadeClimbers has an incredible quantity of HTML tables which seem to move around unpredictably.
    # Use the distinctive 'Location|Route' header link to find the right table.
    location_header = html.xpath('.//a[contains(text(),"Location|Route")]')[0]
    results_table = location_header.getparent().getparent().getparent()

    cascadeclimbers_reports = get_basic_data_from_table(results_table, 2)
    base_url = results_response.geturl()
    reports_in_standardized_format = [
        _cascadeclimbers_data_to_trip_report_summary(report, base_url)
        for report in cascadeclimbers_reports
    ]

    return reports_in_standardized_format
