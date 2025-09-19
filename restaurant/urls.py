# restaurant/urls.py
# Aidan Xu (axu26@bu.edu), 9/16/25
# A web app specific url.py file separate from the cs412 one for restaurant app

from django.urls import path
from django.conf import settings
from . import views

# the web app specific urls for restaurant
urlpatterns = [
    path(r'', views.main, name="main"),
    path(r'main', views.main, name="main"),
    path(r'order', views.order, name="order"),
    path(r'confirmation', views.confirmation, name="confirmation"),
]