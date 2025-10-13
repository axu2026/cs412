# mini_insta/urls.py
# Aidan Xu (axu26@bu.edu), 9/24/25
# A web app specific url.py file separate from the cs412 one for mini_insta app.

from django.urls import path
from django.conf import settings
from . import views
from .views import *

# the web app specific urls
urlpatterns = [
    path('', ProfileListView.as_view(), name="show_all_profiles"),
    path('profile/<int:pk>', ProfileDetailView.as_view(), name="show_profile"),
    path('post/<int:pk>', PostDetailView.as_view(), name="show_post"),
    path('profile/<int:pk>/create_post', CreatePostView.as_view(), name="create_post"),
    path('profile/<int:pk>/update', UpdateProfileView.as_view(), name="update_profile"),
    path('post/<int:pk>/delete', DeletePostView.as_view(), name="delete_post"),
    path('post/<int:pk>/update', UpdatePostView.as_view(), name="update_post"),
    path('photo/<int:pk>/delete', DeletePhotoView.as_view(), name="delete_photo"),
    path('profile/<int:pk>/followers', ShowFollowersDetailView.as_view(), name="show_followers"),
    path('profile/<int:pk>/following', ShowFollowingDetailView.as_view(), name="show_following"),
]