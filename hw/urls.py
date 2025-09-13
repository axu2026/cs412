from django.urls import path
from django.conf import settings
from . import views

urlpatterns = [
    path(r'', views.home, name="home"),
    path(r'home2', views.home_page, name="home_page"),
]