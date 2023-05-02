from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.search, name='search'),
    path('capitals/', views.get_capitals, name='capitals'),
    path('favorites/', views.get_favorites, name='favorites'),
]