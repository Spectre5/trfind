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

def _parse_result(result, peak):
    title = result['titleNoFormatting']

    if peak.name.lower() not in title.lower():
        return

    # Steph's TR titles include route in parenthesis
    # E.g. "Mount Stuart (North Ridge)"
    regex_route_in_parens = '{} \((.*?)\)'.format(peak.name.lower())
    match = re.search(regex_route_in_parens, title.lower())
    route = match.group(1) if match else ''

    return TripReportSummary(
        site = STEPH_ABEGG_SITE,
        link = result['url'],
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
    url = 'https://www.googleapis.com/customsearch/v1element?key=AIzaSyCVAXiUzRYsML1Pv6RwSG1gunmMikTzQqY&cx=005369887179366237532:sfblfll6xtg&{}'.format(query_string)

    response = requests.get(url)
    results = response.json()['results']

    return _parse_results(results, peak)
