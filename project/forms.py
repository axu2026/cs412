# project/forms.py
# Aidan Xu (axu26@bu.edu) 11/23/25
# provides the forms for the creation of different models

from django import forms
from .models import *
from datetime import datetime
from decimal import Decimal
from django.db.models import Q

class AddPaymentForm(forms.Form):
    """a form to add payment to a sale"""
    amount = forms.DecimalField(min_value=0, decimal_places=2)


class GetDatesForm(forms.Form):
    """a form to get the date ranges and date"""
    from_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    to_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    single_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'})
    )


class CreateCustomerForm(forms.ModelForm):
    """the form to create a new customer account"""

    class Meta:
        """ties the form to the customer model"""
        model = Customer
        fields = ['first_name',
                  'last_name', 
                  'address', 
                  'date_of_birth', 
                  'phone_number', 
                  'email']
        # use built in widget to change dob input
        widgets = {
            'date_of_birth': forms.SelectDateWidget(
                attrs={'class': 'formdate'},
                years=range(1900, datetime.now().year)
            ),
        }
    
    def clean_phone_number(self):
        """makes sure the phone number form field is valid"""

        phone_number = self.cleaned_data.get('phone_number')

        # valid phones only consists of digits and has 10 digits
        if not phone_number.isdigit() or len(phone_number) != 10:
            raise forms.ValidationError("Enter a valid 10 digit phone number")

        return phone_number
        

class CreateDependentForm(forms.ModelForm):
    """the form to create a new dependent"""

    class Meta:
        """tie to form to the dependent model"""
        model = Customer
        fields = ['first_name',
                  'last_name',
                  'date_of_birth']
        # use built in widget to change dob input
        widgets = {
            'date_of_birth': forms.SelectDateWidget(
                attrs={'class': 'formdate'},
                years=range(datetime.now().year-17, datetime.now().year)
            ),
        }


class CreateSaleItemForm(forms.ModelForm):
    """the form to create a new saleitem"""

    class Meta:
        """tie the form to the saleitem model"""
        model = SaleItem
        fields = ['customer']

    def __init__(self, *args, sale=None, item=None, **kwargs):
        """store info in the form"""

        super().__init__(*args, **kwargs)
        self.sale = sale
        self.item = item

        # if we have a sale and the customer exists, find dependents, else nothing
        if sale:
            if sale.customer:
                self.fields['customer'].queryset = Customer.objects.filter(
                    Q(guardian=sale.customer) | Q(pk=sale.customer.pk)
                )
            else:
                self.fields['customer'].queryset = Customer.objects.none()

        # if we dont have a customer reliant item, make it not required
        if item and not item.needs_customer:
            self.fields['customer'].required = False

    def clean(self):
        """validate that there is a customer in a customer required item"""

        cleaned_data = super().clean()
        customer = cleaned_data.get('customer')

        # check if the item needs a customer and if there isnt one
        if self.item and self.item.needs_customer and not customer:
            raise forms.ValidationError("Please select a customer!")
        
        return cleaned_data


class CreateSaleForm(forms.ModelForm):
    """the form to confirm a new sale"""

    class Meta:
        """tie form to sale model"""
        model = Sale
        fields = []


class CreateItemForm(forms.ModelForm):
    """the form to create an item"""

    class Meta:
        """tie the form to the item model"""
        model = Item
        fields = ['name', 'price', 'needs_customer']