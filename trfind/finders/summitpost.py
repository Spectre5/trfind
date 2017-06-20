from urlparse import urljoin
import logging

from dateutil.parser import parse as parse_date
from lxml import etree
import mechanicalsoup
import petl

from trfind.html_table import get_basic_data_from_table
from trfind.models import TripReportSummary

SUMMITPOST_SITE = 'SummitPost'

def _summitpost_data_to_trip_report_summary(summitpost_data, base_url):
    return TripReportSummary(
        site=SUMMITPOST_SITE,
        link=urljoin(base_url, summitpost_data['Link']),
        date=parse_date(summitpost_data['Created']),
        title=summitpost_data['Object Name'],
        route=None,
        has_gps=None,
        has_photos=None
    )


def find(peak):
    browser = mechanicalsoup.StatefulBrowser(soup_config={'features':'lxml'})
    browser.open('http://www.summitpost.org/trip-report/')
    browser.select_form(name='object_list')
    browser['object_name_5'] = peak.name
    try:
        results_response = browser.submit()
    except mechanicalsoup.HTTPError as error:
        logging.error('HTTP Error on submitting summitpost form: {}'.format(str(error)))
        return []

    html = etree.HTML(results_response.read())
    try:
        results_table = html.xpath('//table[@class="srch_results"]')[0]
    except IndexError:
        # No results today
        return []

    summitpost_reports = get_basic_data_from_table(results_table, 1)
    base_url = results_response.geturl()
    reports_in_standardized_format = [
        _summitpost_data_to_trip_report_summary(report, base_url)
        for report in summitpost_reports
    ]

    return reports_in_standardized_format
