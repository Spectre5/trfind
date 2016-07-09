import json
import requests

from trfind.models import DayWeather

def get_weather(peak):
    weather_url = 'http://forecast.weather.gov/MapClick.php?lat={lat}&lon={lon}&FcstType=json'.format(lat=peak.lat, lon=peak.lon)
    response = requests.get(weather_url)
    weather_data = json.loads(response.content)

    days = weather_data.get('time',{}).get('startPeriodName', ())
    temp_labels = weather_data.get('time', {}).get('tempLabel', ())
    icon_links = weather_data.get('data', {}).get('iconLink', ())
    temperatures = weather_data.get('data', {}).get('temperature', ())
    precip_likelihoods = weather_data.get('data', {}).get('pop', ())
    weathers = weather_data.get('data', {}).get('weather', ())
    descriptions = weather_data.get('data', {}).get('text', ())

    weathers = zip(days, temperatures, temp_labels, precip_likelihoods, icon_links, weathers, descriptions)

    return tuple(
        DayWeather(*weather)
        for weather in weathers
    )
