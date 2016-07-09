from collections import namedtuple

Peak = namedtuple('Peak', ['name', 'lat', 'lon'])
TripReportSummary = namedtuple('TripReportSummary', ['site', 'link', 'date', 'title', 'route', 'has_gps', 'has_photos'])
DayWeather = namedtuple('DayWeather', ['day_of_week', 'temperature', 'temperature_label', 'chance_of_precipitation', 'icon_link', 'weather_summary', 'weather_description'])
