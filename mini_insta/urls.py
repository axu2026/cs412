# mini_insta/urls.py
# Aidan Xu (axu26@bu.edu), 9/24/25
# A web app specific url.py file separate from the cs412 one for mini_insta app.

from django.urls import path
from django.conf import settings
from . import views
from .views import ProfileListView, ProfileDetailView

# the web app specific urls
urlpatterns = [
    path('', ProfileListView.as_view(), name="show_all_profiles"),
    path('profile/<int:pk>', ProfileDetailView.as_view(), name="show_profile"),
]