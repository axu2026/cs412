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
import plotly
import plotly.graph_objs as go
from django.db.models.functions import TruncDate
import datetime

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
                context['is_manager'] = context['employee'].is_manager
            
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
                first = ''
                last = ''
                # avoid nil indexing
                if len(name) > 0:
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

        return qs.order_by('-created_at').filter(is_dependent=False)

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
        context['dependents'] = Customer.objects.filter(guardian=customer, is_dependent=True)
        context['sales'] = Sale.objects.filter(customer=customer).order_by('-created_at')
        context['is_employee'] = Employee.objects.filter(user=self.request.user).exists()

        # return list of sales accordingly
        if customer.is_dependent:
            context['sales'] = Sale.objects.filter(customer=customer.guardian).order_by('-created_at')
        else:
            context['sales'] = Sale.objects.filter(customer=customer).order_by('-created_at')

        return context
    

class CustomerCreateView(CreateView):
    """view to create a customer account"""

    form_class = CreateCustomerForm
    template_name = 'project/customer_create.html'

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
    template_name = "project/customer_update.html"
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
    

class DependentCreateView(LoginRequiredMixin, CreateView):
    """view to create a customer dependent"""

    form_class = CreateDependentForm
    template_name = 'project/dependent_create.html'

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
        """provides context for creating a new dependent"""

        # get context and put the guardian
        context = super().get_context_data(**kwargs)
        context['guardian'] = Customer.objects.get(pk=self.kwargs['pk'])

        return context

    def get_success_url(self):
        """return back to the guardian's page"""
        return reverse('customer', kwargs={'pk': self.kwargs['pk']})

    def form_valid(self, form):
        """insert information from guardian"""

        # find guardian and auto fill everything
        guardian = Customer.objects.get(pk=self.kwargs['pk'])
        form.instance.guardian = guardian
        form.instance.is_dependent = True
        form.instance.address = guardian.address
        form.instance.phone_number = guardian.phone_number
        form.instance.email = guardian.email

        return super().form_valid(form)


class DependentUpdateView(LoginRequiredMixin, UpdateView):
    """view to update a customer dependent"""

    form_class = CreateDependentForm
    template_name = 'project/dependent_update.html'
    model = Customer

    def dispatch(self, request, *args, **kwargs):
        """verify the user has permission to view this"""

        # check if the user is authenticated
        if request.user.is_authenticated:
            # the customer of the current page
            dependent = Customer.objects.get(pk=kwargs['pk'])

            # if the user is an employee or is the user of the page, allow to view
            if (Employee.objects.filter(user=self.request.user).exists()
                or dependent.guardian.user == self.request.user):
                return super().dispatch(request, *args, **kwargs)
                
        # else, no permission
        return render(request, "project/no_permission.html")

    def get_login_url(self):
        """redirect to the log in page"""
        return reverse('login')

    def get_success_url(self):
        """return back to the guardian's page"""
        dependent = Customer.objects.get(pk=self.kwargs['pk'])
        return reverse('customer', kwargs={'pk': dependent.guardian.pk})

    def get_context_data(self, **kwargs):
        """provides context for updating a dependent"""

        # get context and put guardian and dependent in
        context = super().get_context_data(**kwargs)
        context['dependent'] = Customer.objects.get(pk=self.kwargs['pk'])

        return context


class DependentDeleteView(LoginRequiredMixin, DeleteView):
    """view to delete a customer dependent"""

    model = Customer
    template_name = 'project/dependent_delete.html'

    def dispatch(self, request, *args, **kwargs):
        """verify the user has permission to view this"""

        # check if the user is authenticated
        if request.user.is_authenticated:
            # the customer of the current page
            dependent = Customer.objects.get(pk=kwargs['pk'])

            # if the user is an employee or is the user of the page, allow to view
            if (Employee.objects.filter(user=self.request.user).exists()
                or dependent.guardian.user == self.request.user):
                return super().dispatch(request, *args, **kwargs)
                
        # else, no permission
        return render(request, "project/no_permission.html")

    def get_login_url(self):
        """redirect to the log in page"""
        return reverse('login')
    
    def get_success_url(self):
        """return back to the guardian's page"""
        dependent = Customer.objects.get(pk=self.kwargs['pk'])
        return reverse('customer', kwargs={'pk': dependent.guardian.pk})

    def get_context_data(self, **kwargs):
        """provides context for updating a dependent"""

        # get context and put guardian and dependent in
        context = super().get_context_data(**kwargs)
        context['dependent'] = Customer.objects.get(pk=self.kwargs['pk'])

        return context


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
   

class SaleListView(LoginRequiredMixin, ListView):
    """list to see all events"""

    model = Sale
    template_name = "project/sale_list.html"
    context_object_name = "sales"
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
                filter = Q(customer__first_name__icontains=query) | Q(customer__last_name__icontains=query)

                # if query is a number, find id
                if query.isdigit():
                    filter |= Q(pk=int(query))

                # apply the filters inclusively
                qs = qs.filter(filter).distinct()

        return qs.order_by('-created_at')

    def get_login_url(self):
        """redirect to the log in page"""
        return reverse('login')


class SaleDetailView(LoginRequiredMixin, DetailView):
    """view to see sale details"""

    template_name = "project/sale_detail.html"
    model = Sale
    context_object_name = "sale"

    def get_login_url(self):
        """redirect to the log in page"""
        return reverse('login')

    def dispatch(self, request, *args, **kwargs):
        """verify the user has permission to view this"""

        # check if the user is authenticated
        if request.user.is_authenticated:
            # get the sale and the customer of the sale
            sale = Sale.objects.get(pk=kwargs['pk'])

            # check if the sale has a customer
            if sale.customer:
                customer = Customer.objects.filter(pk=sale.customer.pk)

                # if so, check for permissions
                if customer and customer.first().user == self.request.user:
                    return super().dispatch(request, *args, **kwargs)

            # if the user is an employee or is the user of the page, allow to view
            if Employee.objects.filter(user=self.request.user).exists():
                return super().dispatch(request, *args, **kwargs)
                
        # else, no permission
        return render(request, "project/no_permission.html")

    def get_context_data(self, **kwargs):
        """return the context for all saleitems"""

        context = super().get_context_data(**kwargs)
        context['form'] = AddPaymentForm()
        sale = Sale.objects.get(pk=self.kwargs['pk'])
        context['total'] = sale.get_total_price()
        context['saleitems'] = SaleItem.objects.filter(sale=sale)

        # find the balance to display it
        context['balance'] = context['total'] - sale.amount_paid

        # check if there is an employee on the view
        if self.request.user.is_authenticated:
            context['is_employee'] = Employee.objects.filter(user=self.request.user).exists()

            # get the list of possible items to sell for the employee
            if context['is_employee']:
                items = Item.objects.all()

                # filter if we have a query
                if 'query' in self.request.GET and self.request.GET['query']:
                    items = items.filter(name__contains=self.request.GET['query'])

                context['items'] = items

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


class SaleCreateView(LoginRequiredMixin, CreateView):
    """view to confirm creating a sale"""

    form_class = CreateSaleForm
    template_name = "project/sale_create.html"
    model = Sale

    def dispatch(self, request, *args, **kwargs):
        """check if the user is an employee so that creation is allowed"""

        customer = Customer.objects.get(pk=self.kwargs['pk'])

        # cant make sales with a dependent
        if customer.is_dependent:
            return render(request, "project/no_permission.html")

        # if the user is authenticated,
        if request.user.is_authenticated:
            # and the user is an employee,
            if Employee.objects.filter(user=self.request.user).exists():
                return super().dispatch(request, *args, **kwargs)

        # permission denied 
        return render(request, "project/no_permission.html")

    def get_login_url(self):
        """redirect to the log in page"""
        return reverse('login')

    def get_context_data(self, **kwargs):
        """find customer and put into context"""

        context = super().get_context_data(**kwargs)
        context["customer"] = Customer.objects.get(pk=self.kwargs['pk'])

        return context
    
    def form_valid(self, form):
        """inject the customer and employee into the form"""

        form.instance.customer = Customer.objects.get(pk=self.kwargs['pk'])
        form.instance.employee = Employee.objects.get(user=self.request.user)
        form.instance.amount_paid = Decimal('0.00')

        return super().form_valid(form)
    

class SaleOpenCreateView(LoginRequiredMixin, CreateView):
    """view to confirm creating a sale"""

    form_class = CreateSaleForm
    template_name = "project/sale_create_open.html"
    model = Sale

    def dispatch(self, request, *args, **kwargs):
        """check if the user is an employee so that creation is allowed"""

        # if the user is authenticated,
        if request.user.is_authenticated:
            # and the user is an employee,
            if Employee.objects.filter(user=self.request.user).exists():
                return super().dispatch(request, *args, **kwargs)

        # permission denied 
        return render(request, "project/no_permission.html")

    def get_login_url(self):
        """redirect to the log in page"""
        return reverse('login')
    
    def form_valid(self, form):
        """inject the customer and employee into the form"""

        form.instance.employee = Employee.objects.get(user=self.request.user)
        form.instance.amount_paid = Decimal('0.00')

        return super().form_valid(form)


class SaleItemCreateView(LoginRequiredMixin, CreateView):
    """view to create a saleitem"""

    form_class = CreateSaleItemForm
    template_name = "project/saleitem_create.html"
    model = SaleItem

    def dispatch(self, request, *args, **kwargs):
        """verify the user has permission to view this"""

        # check if the user is authenticated and is not a staff member
        if request.user.is_authenticated:
            if not Employee.objects.filter(user=self.request.user).exists():
                return render(request, "project/no_permission.html")
        
        return super().dispatch(request, *args, **kwargs)

    def get_login_url(self):
        """redirect to the log in page"""
        return reverse('login')
    
    def get_context_data(self, **kwargs):
        """get the context data for creating a saleitem"""

        context = super().get_context_data(**kwargs)
        context['item'] = Item.objects.get(pk=self.kwargs['item_pk'])
        context['sale'] = Sale.objects.get(pk=self.kwargs['pk'])

        return context
    
    def get_form_kwargs(self):
        """provide the form with the sale and item"""

        # find the sale and item and pass to form
        kwargs = super().get_form_kwargs()
        pk = self.kwargs.get('pk')
        item_pk = self.kwargs.get('item_pk')
        kwargs['sale'] = Sale.objects.get(id=pk)
        kwargs['item'] = Item.objects.get(id=item_pk)

        return kwargs
    
    def form_valid(self, form):
        """inject the item and sale into the form"""

        sale = Sale.objects.get(pk=self.kwargs['pk'])
        item = Item.objects.get(pk=self.kwargs['item_pk'])
        form.instance.sale = sale
        form.instance.item = item
        form.instance.price = item.price
        form.instance.name = item.name

        return super().form_valid(form)
    
    def get_success_url(self):
        """return back to sale page"""
        return reverse('sale', kwargs={'pk':self.kwargs['pk']})


class SaleItemDeleteView(LoginRequiredMixin, DeleteView):
    """view to delete a saleitem from a sale"""

    template_name = "project/saleitem_delete.html"
    model = SaleItem

    def dispatch(self, request, *args, **kwargs):
        """verify the user has permission to view this"""

        # check if the user is authenticated and is not a staff member
        if request.user.is_authenticated:
            if not Employee.objects.filter(user=self.request.user).exists():
                return render(request, "project/no_permission.html")
        
        return super().dispatch(request, *args, **kwargs)

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
    

class ItemDeleteView(LoginRequiredMixin, DeleteView):
    """view to delete an item"""

    template_name = "project/item_delete.html"
    model = Item

    def dispatch(self, request, *args, **kwargs):
        """verify the user has permission to view this"""

        # check if the user is authenticated and is not a staff member
        if request.user.is_authenticated:
            employee = Employee.objects.filter(user=self.request.user)

            # check for employee, if so check if they are a manager
            if not employee or not employee.first().is_manager:
                return render(request, "project/no_permission.html")
        
        return super().dispatch(request, *args, **kwargs)
    
    def get_login_url(self):
        """redirect to the log in page"""
        return reverse('login')
    
    def get_success_url(self):
        """return back to home page"""
        return reverse('items')


class ItemCreateView(LoginRequiredMixin, CreateView):
    """the view for creating a new item"""

    form_class = CreateItemForm
    template_name = "project/item_create.html"
    model = Item

    def dispatch(self, request, *args, **kwargs):
        """verify the user has permission to view this"""

        # check if the user is authenticated and is not a staff member
        if request.user.is_authenticated:
            employee = Employee.objects.filter(user=self.request.user)

            # check for employee, if so check if they are a manager
            if not employee or not employee.first().is_manager:
                return render(request, "project/no_permission.html")
        
        return super().dispatch(request, *args, **kwargs)
    
    def get_login_url(self):
        """redirect to the log in page"""
        return reverse('login')
    
    def get_success_url(self):
        """return back to home page"""
        return reverse('items')
    

class ItemUpdateView(LoginRequiredMixin, UpdateView):
    """view to update an item"""

    form_class = CreateItemForm
    template_name = 'project/item_update.html'
    model = Item

    def dispatch(self, request, *args, **kwargs):
        """verify the user has permission to view this"""

        # check if the user is authenticated and is not a staff member
        if request.user.is_authenticated:
            employee = Employee.objects.filter(user=self.request.user)

            # check for employee, if so check if they are a manager
            if not employee or not employee.first().is_manager:
                return render(request, "project/no_permission.html")
        
        return super().dispatch(request, *args, **kwargs)
    
    def get_login_url(self):
        """redirect to the log in page"""
        return reverse('login')
    
    def get_success_url(self):
        """return back to home page"""
        return reverse('items')
    
    def get_context_data(self, **kwargs):
        """provides context for updating an item"""

        # get context and put guardian and dependent in
        context = super().get_context_data(**kwargs)
        context['item'] = Item.objects.get(pk=self.kwargs['pk'])

        return context


class ItemListView(LoginRequiredMixin, ListView):
    """the view to see all items"""

    model = Item
    template_name = "project/item_list.html"
    context_object_name = "items"

    def dispatch(self, request, *args, **kwargs):
        """verify the user has permission to view this"""

        # check if the user is authenticated and is not a staff member
        if request.user.is_authenticated:
            employee = Employee.objects.filter(user=self.request.user)

            # check for employee, if so check if they are a manager
            if not employee or not employee.first().is_manager:
                return render(request, "project/no_permission.html")
        
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        """apply query filters to the set"""

        qs = super().get_queryset()

        # check if there is a query
        if "query" in self.request.GET and self.request.GET['query']:
            qs = qs.filter(name__contains=self.request.GET['query'])

        return qs

    def get_login_url(self):
        """redirect to the log in page"""
        return reverse('login')


class StatisticsView(ListView):
    """view for seeing statistics"""

    template_name = "project/statistics.html"
    context_object_name = "sales"

    def dispatch(self, request, *args, **kwargs):
        """verify the user has permission to view this"""

        # check if the user is authenticated and is not a staff member
        if request.user.is_authenticated:
            employee = Employee.objects.filter(user=self.request.user)

            # check for employee, if so check if they are a manager
            if not employee or not employee.first().is_manager:
                return render(request, "project/no_permission.html")
        
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        """return a queryset for sales according to query"""

        qs = Sale.objects.all()
        from_date = self.request.GET.get('from_date')
        to_date = self.request.GET.get('to_date')

        # filter the sales by range of date
        if from_date and to_date:
            qs = qs.filter(created_at__gte=from_date)
            qs = qs.filter(created_at__lte=to_date)

        return qs

    def get_context_data(self, **kwargs):
        """return context with graphs"""

        context = super().get_context_data(**kwargs)

        # provide the form with initialized dates if needed
        if not self.request.GET:
            from_date = datetime.date.today() - datetime.timedelta(days=30)
            to_date = datetime.date.today()

            context['form'] = GetDatesForm(initial={
                'from_date': from_date,
                'to_date': to_date,
                'single_date': to_date,
            })
        else:
            context['form'] = GetDatesForm(self.request.GET)

        # for line graph
        # get all days and their total sale revenue
        sales = (
            self.get_queryset()
            .annotate(day=TruncDate("created_at"))
            .values("day")
            .annotate(total=Sum("amount_paid"))
            .order_by("day")
        )

        x = [p["day"] for p in sales]
        y = [p["total"] for p in sales]

        # plot data and return graph
        fig = go.Scatter(x=x, y=y, mode="lines+markers", name="Revenue per day")
        title = 'Revenue of sales per day'
        graph_line = plotly.offline.plot({'data': [fig], 
                                          "layout_title_text": title},
                                          auto_open=False,
                                          output_type='div')
        context['graph_line'] = graph_line

        # for pie graph
        date_single = self.request.GET.get("single_date")

        # if there is not a get request, give default
        if not date_single:
            date_single = datetime.date.today()

        sales_single = (
            SaleItem.objects
            .filter(sale__created_at__date=date_single)
            .select_related("item")
        )

        item_totals = {}

        # go through all sales on that day and store values
        for s in sales_single:
            name = s.name
            price = s.price
            item_totals[name] = item_totals.get(name, 0) + price

        # make the figure and graph
        fig = go.Pie(labels=list(item_totals.keys()), values=list(item_totals.values()))
        title = f'Sale distribution on {date_single}'
        graph_pie = plotly.offline.plot({"data": [fig],
                                            "layout_title_text": title},
                                            auto_open=False,
                                            output_type="div")
        context['graph_pie'] = graph_pie

        return context
    

# API
class CustomerCreateAPIView(generics.CreateAPIView):
    """view for the customer api"""

    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


class DependentCreateAPIView(generics.CreateAPIView):
    """view for the dependent api"""

    queryset = Customer.objects.all()
    serializer_class = DependentSerializer