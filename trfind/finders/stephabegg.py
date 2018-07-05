import json
from datetime import datetime
import re

from bs4 import BeautifulSoup
from dateutil import parser
from functools import partial
import requests
import urllib
from urllib.parse import urljoin, urlencode
from urllib.request import Request, urlopen

from trfind.models import TripReportSummary

STEPH_ABEGG_SITE = 'Steph Abegg'

def remove_mount(title_lowered):
    ''' Page titles incldue stuff like 'mt. stuart' so when we search in the title, remove 'Mount' from our peak name '''
    if title_lowered.startswith('mount'):
        return title_lowered[len('mount'):]

def _parse_result(result, peak):
    title = result['title']

    if remove_mount(peak.name.lower()) not in title.lower():
        print('didnt find', peak.name.lower(), 'in', title.lower())
        return

    # Steph's TR titles include route in parenthesis
    # E.g. "Mount Stuart (North Ridge)"
    regex_route_in_parens = '{} \((.*?)\)'.format(peak.name.lower())
    match = re.search(regex_route_in_parens, title.lower())
    route = match.group(1) if match else ''

    return TripReportSummary(
        site = STEPH_ABEGG_SITE,
        link = result['link'],
        date = None,
        route = route,
        title = title,
        has_gps = False,
        has_photos = False
    )

def _parse_results(results, peak):
    return filter(None, (
        _parse_result(result, peak)
        for result in results
    ))


def find(peak):
    # Use a Google Custom Search engine to search Steph Abegg's site
    query_string = urlencode({
        'q': peak.name
    })
    url = 'https://www.googleapis.com/customsearch/v1?key=AIzaSyCDKkFSe-FgCZdMqyU5vOEgq2T0jgnSxP8&cx=008421871213652748671:uaqmznzb4ys&{}'.format(query_string)

    response = requests.get(url)
    results = response.json()['items']

    return _parse_results(results, peak)
