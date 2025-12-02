# project/views.py
# Aidan Xu (axu26@bu.edu) 11/23/25
# file that defines all of the views for the project app

from django.shortcuts import render
from django.views.generic import *
from django.http import HttpResponseRedirect
from .models import *
from .forms import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import login
from rest_framework import generics
from .serializers import *
from django.contrib.auth.views import LoginView
from django.db.models import Q
from decimal import Decimal

# Create your views here.
class HomeTemplateView(TemplateView):
    """template view for the home page, provides log in links"""

    template_name = "project/home.html"

    def get_context_data(self, **kwargs):
        """get either the customer or employee"""

        context = super().get_context_data(**kwargs)
        
        # check if there is an authenticated user
        if self.request.user.is_authenticated:
            # if the user is an employee, find the employee model
            employee = Employee.objects.filter(user=self.request.user)
            if employee:
                context['employee'] = employee.first()
            
            # if the user is a customer, find the customer model
            customer = Customer.objects.filter(user=self.request.user)
            if customer:
                context['customer'] = customer.first()

        return context


class CustomerListView(LoginRequiredMixin, ListView):
    """list view to show the list of customers"""

    model = Customer
    template_name = "project/customer_list.html"
    context_object_name = "customers"
    paginate_by = 10

    def dispatch(self, request, *args, **kwargs):
        """verify the user has permission to view this"""

        # check if the user is authenticated and is not a staff member
        if request.user.is_authenticated:
            if not Employee.objects.filter(user=self.request.user).exists():
                return render(request, "project/no_permission.html")
        
        return super().dispatch(request, *args, **kwargs)
    
    def get_queryset(self):
        """apply filters before returning the queryset"""

        qs = super().get_queryset()

        # filter the queryset according to the search query
        # check if query is in the get request
        if 'query' in self.request.GET:
            query = self.request.GET['query']

            # check if query is not null
            if query:
                name = query.split()
                first = name[0]
                last = name[-1]

                # apply the filters inclusively
                qs = qs.filter(
                    Q(first_name__icontains=first, last_name__icontains=last) |
                    Q(first_name__icontains=query) |
                    Q(last_name__icontains=query) |
                    Q(address__icontains=query) |
                    Q(phone_number__icontains=query) |
                    Q(email__icontains=query)
                ).distinct()

        return qs

    def get_login_url(self):
        """redirect to the log in page"""
        return reverse('login')


class CustomerDetailView(LoginRequiredMixin, DetailView):
    """view to show details of a customer and their history"""

    model = Customer
    template_name = "project/customer_detail.html"
    context_object_name = "customer"

    def dispatch(self, request, *args, **kwargs):
        """verify the user has permission to view this"""

        # check if the user is authenticated
        if request.user.is_authenticated:
            # the customer of the current page
            customer = Customer.objects.get(pk=kwargs['pk'])

            # if the user is an employee or is the user of the page, allow to view
            if (Employee.objects.filter(user=self.request.user).exists()
                or customer.user == self.request.user):
                return super().dispatch(request, *args, **kwargs)
                
        # else, no permission
        return render(request, "project/no_permission.html")

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

    def dispatch(self, request, *args, **kwargs):
        """verify the user has permission to view this"""

        # check if the user is authenticated
        if request.user.is_authenticated:
            # the customer of the current page
            customer = Customer.objects.get(pk=kwargs['pk'])

            # if the user is an employee or is the user of the page, allow to view
            if (Employee.objects.filter(user=self.request.user).exists()
                or customer.user == self.request.user):
                return super().dispatch(request, *args, **kwargs)
                
        # else, no permission
        return render(request, "project/no_permission.html")

    def get_login_url(self):
        """redirect to the log in page"""
        return reverse('login')
    

class CustomLoginView(LoginView):
    """custom loginview for custom redirect"""

    template_name = "project/login.html"

    def get_success_url(self):
        """redirect to a page depending on who it is"""

        # check if there is an authenticated user
        if self.request.user.is_authenticated:
            # if the user is an employee, find the employee model
            employee = Employee.objects.filter(user=self.request.user)
            if employee:
                return reverse('home')
            
            # if the user is a customer, find the customer model
            customer = Customer.objects.filter(user=self.request.user)
            if customer:
                c = customer.first()
                return reverse('customer', kwargs={"pk": c.pk})

        return reverse('home')


class DependentCreateView(LoginRequiredMixin, CreateView):
    """view to create a new dependent"""

    form_class = CreateDependentForm
    template_name = "project/create_dependent.html"
    model = Dependent

    def dispatch(self, request, *args, **kwargs):
        """verify the user has permission to view this"""

        # check if the user is authenticated
        if request.user.is_authenticated:
            # the customer of the current page
            customer = Customer.objects.get(pk=kwargs['pk'])

            # if the user is an employee or is the user of the page, allow to view
            if (Employee.objects.filter(user=self.request.user).exists()
                or customer.user == self.request.user):
                return super().dispatch(request, *args, **kwargs)
                
        # else, no permission
        return render(request, "project/no_permission.html")

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

    def dispatch(self, request, *args, **kwargs):
        """verify the user has permission to view this"""

        # check if the user is authenticated
        if request.user.is_authenticated:
            # the guardian of the dependent
            dependent = Dependent.objects.get(pk=kwargs['pk'])
            customer = Customer.objects.get(pk=dependent.guardian.pk)

            # if the user is an employee or is the user of the page, allow to view
            if (Employee.objects.filter(user=self.request.user).exists()
                or customer.user == self.request.user):
                return super().dispatch(request, *args, **kwargs)
                
        # else, no permission
        return render(request, "project/no_permission.html")

    def get_login_url(self):
        """redirect to the log in page"""
        return reverse('login')
    
    def get_context_data(self, **kwargs):
        """get the context data for updating a dependent"""

        context = super().get_context_data(**kwargs)
        context['dependent'] = Dependent.objects.get(pk=self.kwargs['pk'])

        return context
    
    def get_success_url(self):
        """return back to customer page"""
        dependent = Dependent.objects.get(pk=self.kwargs['pk'])
        return reverse('customer', kwargs={'pk':dependent.guardian.pk})
    

class DependentDeleteView(LoginRequiredMixin, DeleteView):
    """view to delete a dependent"""

    template_name = "project/delete_dependent.html"
    model = Dependent

    def dispatch(self, request, *args, **kwargs):
        """verify the user has permission to view this"""

        # check if the user is authenticated
        if request.user.is_authenticated:
            # the guardian of the dependent
            dependent = Dependent.objects.get(pk=kwargs['pk'])
            customer = Customer.objects.get(pk=dependent.guardian.pk)

            # if the user is an employee or is the user of the page, allow to view
            if (Employee.objects.filter(user=self.request.user).exists()
                or customer.user == self.request.user):
                return super().dispatch(request, *args, **kwargs)
                
        # else, no permission
        return render(request, "project/no_permission.html")

    def get_login_url(self):
        """redirect to the log in page"""
        return reverse('login')
    
    def get_context_data(self, **kwargs):
        """get the context data for updating a dependent"""

        context = super().get_context_data(**kwargs)
        context['dependent'] = Dependent.objects.get(pk=self.kwargs['pk'])

        return context
    
    def get_success_url(self):
        """return back to customer page"""
        dependent = Dependent.objects.get(pk=self.kwargs['pk'])
        return reverse('customer', kwargs={'pk':dependent.guardian.pk})
    

class SaleDetailView(LoginRequiredMixin, DetailView):
    """view to see sale details"""

    template_name = "project/sale_detail.html"
    model = Sale
    context_object_name = "sale"

    def dispatch(self, request, *args, **kwargs):
        """verify the user has permission to view this"""

        # check if the user is authenticated
        if request.user.is_authenticated:
            # get the sale and the customer of the sale
            sale = Sale.objects.get(pk=kwargs['pk'])
            customer = Customer.objects.get(pk=sale.customer.pk)

            # if the user is an employee or is the user of the page, allow to view
            if (Employee.objects.filter(user=self.request.user).exists()
                or customer.user == self.request.user):
                return super().dispatch(request, *args, **kwargs)
                
        # else, no permission
        return render(request, "project/no_permission.html")

    def get_context_data(self, **kwargs):
        """return the context for all saleitems"""

        context = super().get_context_data(**kwargs)
        context['form'] = AddPaymentForm()
        sale = Sale.objects.get(pk=self.kwargs['pk'])
        context['total'] = sale.get_total_price()

        # find the balance to display it
        context['balance'] = context['total'] - sale.amount_paid

        # check if there is an employee on the view
        if self.request.user.is_authenticated:
            context['is_employee'] = Employee.objects.filter(user=self.request.user).exists()

            # get the list of possible items to sell for the employee
            if context['is_employee']:
                context['items'] = Item.objects.all()

        return context
    
    def post(self, request, *args, **kwargs):
        """handle adding payment form"""

        sale = self.get_object()
        form = AddPaymentForm(request.POST)

        # ensure the form is valid before we add the amount
        if form.is_valid():
            amount = form.cleaned_data['amount']
            sale.amount_paid += amount
            sale.save()

        return HttpResponseRedirect(reverse('sale', kwargs={'pk':self.kwargs['pk']}))
    

class SaleItemCreateView(LoginRequiredMixin, CreateView):
    """view to create a saleitem"""

    form_class = CreateSaleItemForm
    template_name = "project/create_saleitem.html"
    model = SaleItem

    def dispatch(self, request, *args, **kwargs):
        """verify the user has permission to view this"""

        # check if the user is authenticated
        if request.user.is_authenticated:
            # get the sale and the customer of the sale
            sale = Sale.objects.get(pk=kwargs['pk'])
            customer = Customer.objects.get(pk=sale.customer.pk)

            # if the user is an employee or is the user of the page, allow to view
            if (Employee.objects.filter(user=self.request.user).exists()
                or customer.user == self.request.user):
                return super().dispatch(request, *args, **kwargs)
                
        # else, no permission
        return render(request, "project/no_permission.html")

    def get_login_url(self):
        """redirect to the log in page"""
        return reverse('login')
    
    def get_context_data(self, **kwargs):
        """get the context data for creating a saleitem"""

        context = super().get_context_data(**kwargs)
        context['item'] = Item.objects.get(pk=self.kwargs['item_pk'])
        context['sale'] = Sale.objects.get(pk=self.kwargs['pk'])

        return context
    
    def form_valid(self, form):
        """inject the item and sale into the form"""

        sale = Sale.objects.get(pk=self.kwargs['pk'])
        item = Item.objects.get(pk=self.kwargs['item_pk'])
        form.instance.sale = sale
        form.instance.item = item
        form.instance.price = item.price

        return super().form_valid(form)
    
    def get_success_url(self):
        """return back to sale page"""
        return reverse('sale', kwargs={'pk':self.kwargs['pk']})


class SaleItemDeleteView(LoginRequiredMixin, DeleteView):
    """view to delete a saleitem from a sale"""

    template_name = "project/delete_saleitem.html"
    model = SaleItem

    def dispatch(self, request, *args, **kwargs):
        """verify the user has permission to view this"""

        # check if the user is authenticated
        if request.user.is_authenticated:
            # get the sale and the customer of the sale
            saleitem = SaleItem.objects.get(pk=kwargs['pk'])
            customer = Customer.objects.get(pk=saleitem.sale.customer.pk)

            # if the user is an employee or is the user of the page, allow to view
            if (Employee.objects.filter(user=self.request.user).exists()
                or customer.user == self.request.user):
                return super().dispatch(request, *args, **kwargs)
                
        # else, no permission
        return render(request, "project/no_permission.html")

    def get_login_url(self):
        """redirect to the log in page"""
        return reverse('login')
    
    def get_success_url(self):
        """return back to customer page"""
        saleitem = SaleItem.objects.get(pk=self.kwargs['pk'])
        return reverse('sale', kwargs={'pk':saleitem.sale.pk})
    
    def get_context_data(self, **kwargs):
        """get the saleitem in question"""

        context = super().get_context_data(**kwargs)
        context['saleitem'] = SaleItem.objects.get(pk=self.kwargs['pk'])

        return context