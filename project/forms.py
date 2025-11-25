# project/forms.py
# Aidan Xu (axu26@bu.edu) 11/23/25
# provides the forms for the creation of different models

from django import forms
from .models import *

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
        model = Dependent
        fields = ['first_name',
                  'last_name',
                  'date_of_birth']