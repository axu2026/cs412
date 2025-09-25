# mini_insta/views.py
# Aidan Xu (axu26@bu.edu), 9/24/25
# The views code used for the mini_insta app

from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.views.generic import ListView, DetailView
from .models import Profile

# Create your views here.
class ProfileListView(ListView):
    """A view class to show all profiles"""

    model = Profile
    template_name = "mini_insta/show_all_profiles.html"
    context_object_name = "profiles" # all profiles

class ProfileDetailView(DetailView):
    """A view class to show more details of a single profile"""

    model = Profile
    template_name = "mini_insta/show_profile.html"
    context_object_name = "profile" # single profile