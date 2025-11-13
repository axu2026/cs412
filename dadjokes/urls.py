# dadjokes/urls.py
# aidan xu (axu26@bu.edu) 11/11/2025
# the app specific url patterns for the dadjokes application

from django.urls import path
from .views import *

urlpatterns = [
    path('', RandomTemplateView.as_view(), name="home"),
    path('random', RandomTemplateView.as_view(), name="random"),
    path('jokes', JokeListView.as_view(), name="joke_list"),
    path('joke/<int:pk>', JokeDetailView.as_view(), name="joke_detail"),
    path('pictures', PictureListView.as_view(), name="picture_list"),
    path('picture/<int:pk>', PictureDetailView.as_view(), name="picture_detail"),
    # api paths
    path('api/', RandomAPIView.as_view(), name="api"),
    path('api/jokes', JokeListAPIView.as_view(), name="api_joke_list"),
    path('api/joke/<int:pk>', JokeAPIView.as_view(), name="api_joke"),
    path('api/pictures', PictureListAPIView.as_view(), name="api_picture_list"),
    path('api/picture/<int:pk>', PictureAPIView.as_view(), name="api_picture"),
    path('api/random', RandomAPIView.as_view(), name="api_random"),
]