from urlparse import urljoin

from dateutil.parser import parse as parse_date
from lxml import etree
import mechanize
import petl

from trfind.models import TripReportSummary


SUMMITPOST_SITE = 'SummitPost'


def _get_some_text_content(table_cell_node):
    ''' Remove all the links and crap and just return a simplified contents string
    '''
    try: 
        title = table_cell_node.text.strip()
        if title:
            return title
    except AttributeError:
        pass # No content at the top level; we need to go deeper

    children = table_cell_node.getchildren()
    for child in children:
        # Sometimes there are multiple links and stuff; the real name is in the first element that works
        try:
            return _get_some_text_content(child)
        except AttributeError:
            continue


def _get_first_link_target(node):
    return node.find('a').attrib['href']


def _get_report_data_from_row(results_row, headers):
    values = [_get_some_text_content(col) for col in results_row]
    data = dict(zip(headers, values))
    data['Relative link'] = _get_first_link_target(results_row[1])
    return data


def _get_report_data_from_table(table_node):
    rows = iter(table_node.findall('tr'))
    headers = [_get_some_text_content(col) for col in next(rows)]

    return [
        _get_report_data_from_row(row, headers)
        for row in rows
    ]


def _summitpost_data_to_trip_report_summary(summitpost_data, base_url):
    return TripReportSummary(
        site=SUMMITPOST_SITE,
        link=urljoin(base_url, summitpost_data['Relative link']),
        date=parse_date(summitpost_data['Created']),
        title=summitpost_data['Object Name'],
        route=None,
        has_gps=None,
        has_photos=None
    )


def find(peak):
    peak_name = peak.name
    browser = mechanize.Browser()
    browser.open('http://www.summitpost.org/trip-report/')
    browser.select_form(name='object_list')
    browser['object_name_5'] = peak_name
    results_response = browser.submit()

    html = etree.HTML(results_response.read())
    try:
        results_table = html.xpath('//table[@class="srch_results"]')[0]
    except IndexError:
        # No results today
        return []

    summitpost_reports = _get_report_data_from_table(results_table)
    base_url = results_response.geturl()
    reports_in_standardized_format = [
        _summitpost_data_to_trip_report_summary(report, base_url)
        for report in summitpost_reports
    ]

    return reports_in_standardized_format
