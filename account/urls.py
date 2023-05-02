from django.urls import path

from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('favorite/', views.favorite_location, name='favorite')
]