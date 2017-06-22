import urllib
from urlparse import urljoin
import logging

from dateutil.parser import parse as parse_date
from lxml import etree
import petl

from trfind.finders.shared import clean_peak_name
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


def _summitpost_url_format(peak_name):
    query_string = urllib.urlencode({'object_name_5': peak_name})
    return (
        'http://www.summitpost.org/object_list.php?object_type=5&{}'
        .format(query_string)
    )


def find(peak):
    response = urllib.urlopen(_summitpost_url_format(
        peak_name=clean_peak_name(peak.name)
    ))

    html = etree.HTML(response.read())
    try:
        results_table = html.xpath('//table[@class="srch_results"]')[0]
    except IndexError:
        # No results today
        return []

    summitpost_reports = get_basic_data_from_table(results_table, 1)
    base_url = response.geturl()
    reports_in_standardized_format = [
        _summitpost_data_to_trip_report_summary(report, base_url)
        for report in summitpost_reports
    ]

    return reports_in_standardized_format
