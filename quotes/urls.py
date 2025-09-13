# urls.py
# Aidan Xu (axu26@bu.edu), 9/9/25
# A web app specific url.py file separate from the cs412 one for quotes app.

from django.urls import path
from django.conf import settings
from . import views

# the web app specific urls for quotes
urlpatterns = [
    path(r'', views.quote, name="quote"),
    path(r'quote', views.quote, name="quote"),
    path(r'show_all', views.show_all, name="show_all"),
    path(r'about', views.about, name="about"),
]