# mini_insta/urls.py
# Aidan Xu (axu26@bu.edu), 9/24/25
# A web app specific url.py file separate from the cs412 one for mini_insta app.

from django.urls import path
from django.conf import settings
from . import views
from .views import *
from django.contrib.auth import views as auth_views

# the web app specific urls
urlpatterns = [
    path('', ProfileListView.as_view(), name="show_all_profiles"),
    path('login/', auth_views.LoginView.as_view(template_name='mini_insta/login.html'), name="login"),
    path('logout/', auth_views.LogoutView.as_view(next_page="logout_confirmation"), name="logout"),
    path('logout/confirmation/', LoggedOutView.as_view(), name="logout_confirmation"),
    path('create_profile/', CreateProfileView.as_view(), name="create_profile"),
    path('profile/<int:pk>', ProfileDetailView.as_view(), name="show_profile"),
    path('profile/create_post', CreatePostView.as_view(), name="create_post"),
    path('profile/update', UpdateProfileView.as_view(), name="update_profile"),
    path('profile/feed', PostFeedListView.as_view(), name="show_feed"),
    path('profile/search', SearchView.as_view(), name="search"),
    path('profile/<int:pk>/follow', CreateFollowView.as_view(), name="create_follow"),
    path('profile/<int:pk>/delete_follow', DeleteFollowView.as_view(), name="delete_follow"),
    path('profile/<int:pk>/followers', ShowFollowersDetailView.as_view(), name="show_followers"),
    path('profile/<int:pk>/following', ShowFollowingDetailView.as_view(), name="show_following"),
    path('post/<int:pk>', PostDetailView.as_view(), name="show_post"),
    path('post/<int:pk>/delete', DeletePostView.as_view(), name="delete_post"),
    path('post/<int:pk>/update', UpdatePostView.as_view(), name="update_post"),
    path('photo/<int:pk>/delete', DeletePhotoView.as_view(), name="delete_photo"),
]