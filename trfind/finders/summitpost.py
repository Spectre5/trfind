from datetime import datetime

from trfind.models import TripReportSummary


def find(peak):
    return [
        TripReportSummary(
            site='SummitPost',
            link='www.google.com',
            date=datetime.now(),
            title='Fake item',
            route=None,
            has_gps=None,
            has_photos=None
        )
    ]
