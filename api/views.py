import json
import requests

from django.shortcuts import render, HttpResponse

from djweather.settings import WEATHER_API_KEY, GEOLOCATION_API_KEY


def home(request):
    city = find_location(request)
    if city != None:
        response = requests.get(
            f'https://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q={city}&aqi=yes')
        response = response.json()
        return render(request, "home.html", {
            'location': response['location']['name'],
            'localtime': response['location']['localtime'],
            'temperature': response['current']['temp_c'],
            'feels_like': response['current']['feelslike_c'],
            'condition': response['current']['condition']['text'],
            'icon': response['current']['condition']['icon'],
            'wind': response['current']['wind_kph'],
            'wind_direction': response['current']['wind_dir'],
            'humidity': response['current']['humidity'],
            'uv_index': response['current']['uv'],
            'air_quality': response['current']['air_quality']['us-epa-index'] })
    return render(request, 'home.html')


def search(request):
    if request.method == 'GET':
        city = request.GET.get('city')

        if city == '':
            city = find_location(request)
        elif city != None:
            response = requests.get(
                f'https://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q={city}&aqi=no')
            response = response.json()
            return render(request, "search.html", {
                'search': True,
                'location': response['location']['name'],
                'localtime': response['location']['localtime'],
                'temperature': response['current']['temp_c'],
                'feels_like': response['current']['feelslike_c'],
                'condition': response['current']['condition']['text'],
                'icon': response['current']['condition']['icon'],
                'wind': response['current']['wind_kph'],
                'wind_direction': response['current']['wind_dir'],
                'humidity': response['current']['humidity'],
                'uv_index': response['current']['uv'] })
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
        response = requests.get(
            f'https://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q={city}&aqi=no')
        response = response.json()
        capitals[city] = {
                'location': response['location']['name'],
                'country': response['location']['country'],
                'localtime': response['location']['localtime'],
                'temperature': response['current']['temp_c'],
                'feels_like': response['current']['feelslike_c'],
                'condition': response['current']['condition']['text'],
                'icon': response['current']['condition']['icon'],
                'wind': response['current']['wind_kph'],
                'wind_direction': response['current']['wind_dir'],
                'humidity': response['current']['humidity'],
                'uv_index': response['current']['uv'] }
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