from collections import namedtuple

Peak = namedtuple('Peak', ['name', 'lat', 'lon'])
TripReportSummary = namedtuple('TripReportSummary', ['site', 'link', 'date', 'title', 'route', 'has_gps', 'has_photos'])
