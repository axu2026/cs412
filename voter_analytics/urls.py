# voter_analytics/urls.py
# Aidan Xu (axu26@bu.edu), 10/30/25
# A web app specific url.py file separate from the cs412 one for voter_analytics app.

from django.urls import path
from django.conf import settings
from . import views
from .views import *

# the web app specific urls
urlpatterns = [
    path('', VoterListView.as_view(), name="voters"),
    path('voter/<int:pk>', VoterDetailView.as_view(), name="voter"),
    path('graphs', GraphListView.as_view(), name="graphs"),
]