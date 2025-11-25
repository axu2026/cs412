# project/urls.py
# Aidan Xu (axu26@bu.edu) 11/23/25
# a web app specific url.py file separate from the cs412 one for the project

from django.urls import path
from django.conf import settings
from .views import *
from django.contrib.auth import views as auth_views

# the web app specific urls
urlpatterns = [
    path('', HomeTemplateView.as_view(), name="home"),
    path('create_customer', CustomerCreateView.as_view(), name="create_customer"),
    path('customers', CustomerListView.as_view(), name="customers"),
    path('customer/<int:pk>', CustomerDetailView.as_view(), name="customer"),
    path('customer/<int:pk>/add_dependent', DependentCreateView.as_view(), name="create_dependent"),
    path('customer/<int:pk>/update', CustomerUpdateView.as_view(), name="update_customer"),
    path('customer/<int:customer_pk>/dependent/<int:pk>', DependentUpdateView.as_view(), name="update_dependent"),
    path('login', auth_views.LoginView.as_view(template_name="project/login.html"), name="login"),
    path('logout', auth_views.LogoutView.as_view(next_page="home"), name="logout"),
]