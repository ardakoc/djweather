import json
import requests

from django.shortcuts import render, HttpResponse

from djweather.settings import WEATHER_API_KEY, GEOLOCATION_API_KEY


def get_location_data(request, city):
    response = requests.get(
        f'https://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q={city}&aqi=yes')
    response = response.json()
    return response['location']


def get_current_weather_data(request, city):
    response = requests.get(
        f'https://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q={city}&aqi=yes')
    response = response.json()
    return response['current']


def get_astronomy_data(request, city):
    response = requests.get(
        f'https://api.weatherapi.com/v1/astronomy.json?key={WEATHER_API_KEY}&q={city}&dt=')
    response = response.json()
    return response['astronomy']['astro']


def home(request):
    city = find_location(request)
    if city != None:
        location = get_location_data(request, city)
        current = get_current_weather_data(request, city)
        astronomy = get_astronomy_data(request, city)

        return render(request, "home.html", {
            'location': location['name'],
            'localtime': location['localtime'],
            'temperature': current['temp_c'],
            'feels_like': current['feelslike_c'],
            'condition': current['condition']['text'],
            'icon': current['condition']['icon'],
            'wind': current['wind_kph'],
            'wind_direction': current['wind_dir'],
            'humidity': current['humidity'],
            'uv_index': current['uv'],
            'air_quality': current['air_quality']['us-epa-index'],
            'sunrise': astronomy['sunrise'],
            'sunset': astronomy['sunset'] })
    return render(request, 'home.html')


def search(request):
    if request.method == 'GET':
        city = request.GET.get('city')

        if city == '':
            city = find_location(request)
        elif city != None:
            location = get_location_data(request, city)
            current = get_current_weather_data(request, city)
            astronomy = get_astronomy_data(request, city)

            return render(request, "search.html", {
                'search': True,
                'location': location['name'],
                'localtime': location['localtime'],
                'temperature': current['temp_c'],
                'feels_like': current['feelslike_c'],
                'condition': current['condition']['text'],
                'icon': current['condition']['icon'],
                'wind': current['wind_kph'],
                'wind_direction': current['wind_dir'],
                'humidity': current['humidity'],
                'uv_index': current['uv'],
                'air_quality': current['air_quality']['us-epa-index'],
                'sunrise': astronomy['sunrise'],
                'sunset': astronomy['sunset'] })
        return render(request, 'search.html')
    

def get_capitals(request):
    cities = [
        'Washington DC',
        'London',
        'Rome',
        'Paris',
        'Madrid',
        'Moscow',
        'Berlin',
        'Amsterdam',
        'Bern',
        'Ankara',
        'Sydney',
        'Abu Dhabi',
        'Doha',
        'Riyadh',
        'Jerusalem',
        'Beijing',
        'Tokyo',
        'Ottawa',
        'Buenos Aires',
        'New Delhi',
    ]

    capitals = {}
    for city in cities:        
        location = get_location_data(request, city)
        current = get_current_weather_data(request, city)
        astronomy = get_astronomy_data(request, city)

        capitals[city] = {
                'location': location['name'],
                'country': location['country'],
                'localtime': location['localtime'],
                'temperature': current['temp_c'],
                'feels_like': current['feelslike_c'],
                'condition': current['condition']['text'],
                'icon': current['condition']['icon'],
                'wind': current['wind_kph'],
                'wind_direction': current['wind_dir'],
                'humidity': current['humidity'],
                'uv_index': current['uv'],                 
                'air_quality': current['air_quality']['us-epa-index'],
                'sunrise': astronomy['sunrise'],
                'sunset': astronomy['sunset'] }
    return render(request, 'capitals.html', {'capitals': capitals})
    

def find_location(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')   

    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')    

    geolocation_json = get_geolocation_data(ip)
    geolocation_data = json.loads(geolocation_json)
    city = geolocation_data['city']
    return city


def get_geolocation_data(ip_address):
    # not using the incoming IP address for testing
    api_url = f'https://ipgeolocation.abstractapi.com/v1/?api_key={GEOLOCATION_API_KEY}'
    # response = requests.get(f'{api_url}&ip_address={ip_address}')
    response = requests.get(f'{api_url}')
    return response.content