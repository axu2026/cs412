# project/views.py
# Aidan Xu (axu26@bu.edu) 11/23/25
# file that defines all of the views for the project app

from django.shortcuts import render
from django.views.generic import *
from .models import *
from .forms import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import login
from rest_framework import generics
from .serializers import *

# Create your views here.
class HomeTemplateView(TemplateView):
    """template view for the home page, provides log in links"""

    template_name = "project/home.html"


class CustomerListView(LoginRequiredMixin, ListView):
    """list view to show the list of customers"""

    model = Customer
    template_name = "project/customer_list.html"
    context_object_name = "customers"
    paginate_by = 20

    def get_login_url(self):
        """redirect to the log in page"""
        return reverse('login')


class CustomerDetailView(LoginRequiredMixin, DetailView):
    """view to show details of a customer and their history"""

    model = Customer
    template_name = "project/customer_detail.html"
    context_object_name = "customer"

    def get_login_url(self):
        """redirect to the log in page"""
        return reverse('login')

    def get_context_data(self, **kwargs):
        """get the context data for a customer's detailview"""

        # get the parent context and add in the dependents and sales
        context = super().get_context_data(**kwargs)
        customer = Customer.objects.get(pk=self.kwargs['pk'])
        context['dependents'] = Dependent.objects.filter(guardian=customer)
        context['sales'] = Sale.objects.filter(customer=customer)

        return context
    

class CustomerCreateView(CreateView):
    """view to create a customer account"""

    form_class = CreateCustomerForm
    template_name = 'project/create_customer.html'

    def get_context_data(self, **kwargs):
        """provides context for a second form to create a user"""

        # get context and insert user form into context
        context = super().get_context_data(**kwargs)
        form_user = UserCreationForm()
        context['form_user'] = form_user

        return context
    
    def form_valid(self, form):
        """create user and provide it in customer form to create customer model"""

        # create the user from the user form and log in with it
        form_user = UserCreationForm(self.request.POST)
        user = form_user.save()
        login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')

        # add the user into the customer form
        form.instance.user = user

        return super().form_valid(form)
    

class CustomerUpdateView(LoginRequiredMixin, UpdateView):
    """view to update a customer model"""

    form_class = CreateCustomerForm
    template_name = "project/update_customer.html"
    model = Customer

    def get_login_url(self):
        """redirect to the log in page"""
        return reverse('login')
    

class DependentCreateView(LoginRequiredMixin, CreateView):
    """view to create a new dependent"""

    form_class = CreateDependentForm
    template_name = "project/create_dependent.html"
    model = Dependent

    def get_login_url(self):
        """redirect to the log in page"""
        return reverse('login')
    
    def get_context_data(self, **kwargs):
        """get the context data for creating a dependent"""

        context = super().get_context_data(**kwargs)
        context['customer'] = Customer.objects.get(pk=self.kwargs['pk'])

        return context
    
    def form_valid(self, form):
        """inject the customer guardian into dependent form"""

        guardian = Customer.objects.get(pk=self.kwargs['pk'])
        form.instance.guardian = guardian

        return super().form_valid(form)
    
    def get_success_url(self):
        """return back to customer page"""
        return reverse('customer', kwargs={'pk':self.kwargs['pk']})
    

class DependentUpdateView(LoginRequiredMixin, UpdateView):
    """view to update a dependent"""

    form_class = CreateDependentForm
    template_name = "project/update_dependent.html"
    model = Dependent

    def get_login_url(self):
        """redirect to the log in page"""
        return reverse('login')
    
    def get_context_data(self, **kwargs):
        """get the context data for updating a dependent"""

        context = super().get_context_data(**kwargs)
        context['customer'] = Customer.objects.get(pk=self.kwargs['customer_pk'])

        return context
    
    def get_success_url(self):
        """return back to customer page"""
        return reverse('customer', kwargs={'pk':self.kwargs['customer_pk']})