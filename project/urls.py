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
    path('create_item', ItemCreateView.as_view(), name="create_item"),
    path('customers', CustomerListView.as_view(), name="customers"),
    path('customer/<int:pk>', CustomerDetailView.as_view(), name="customer"),
    path('customer/<int:pk>/update', CustomerUpdateView.as_view(), name="update_customer"),
    path('customer/<int:pk>/create_sale', SaleCreateView.as_view(), name="create_sale"),
    path('customer/<int:pk>/create_dependent', DependentCreateView.as_view(), name="create_dependent"),
    path('dependent/<int:pk>', DependentUpdateView.as_view(), name="update_dependent"),
    path('dependent/<int:pk>/delete', DependentDeleteView.as_view(), name="delete_dependent"),
    path('login', CustomLoginView.as_view(), name="login"),
    path('logout', auth_views.LogoutView.as_view(next_page="home"), name="logout"),
    path('sale/<int:pk>', SaleDetailView.as_view(), name="sale"),
    path('sale/<int:pk>/add/<int:item_pk>', SaleItemCreateView.as_view(), name="create_saleitem"),
    path('saleitem/<int:pk>', SaleItemDeleteView.as_view(), name="delete_saleitem"),
    path('statistics', StatisticsView.as_view(), name="statistics"),
    path('items', ItemListView.as_view(), name="items"),
    path('item/<int:pk>', ItemUpdateView.as_view(), name="update_item"),
    path('item/<int:pk>/delete', ItemDeleteView.as_view(), name="delete_item"),
    path('api/customer/create', CustomerCreateAPIView.as_view(), name="customer_create_api"),
]