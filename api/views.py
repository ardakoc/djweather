import requests

from django.shortcuts import render

from djweather.settings import API_KEY


def weather(request):
    if request.method == 'GET':
        city = request.GET.get('city')
        if city != None:
            response = requests.get(
                f'https://api.weatherapi.com/v1/current.json?key={API_KEY}&q={city}&aqi=no')
            weather = response.json()
            return render(request, "index.html", {'weather': weather})
        return render(request, "index.html")