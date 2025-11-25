# project/models.py
# Aidan Xu (axu26@bu.edu) 11/23/25
# defines all the models to be used for the project db

from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.
class Customer(models.Model):
    """defines the customer model with its fields and methods"""

    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    date_of_birth = models.DateField()
    address = models.CharField(max_length=128)
    phone_number = models.CharField(max_length=10)
    email = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        """return the string representation of the customer"""
        return f'{self.first_name} {self.last_name}'

    def get_absolute_url(self):
        """return the url path to a particular customer model"""
        return reverse('customer', kwargs={'pk':self.pk})


class Dependent(models.Model):
    """defines the dependent model with its fields and methods"""

    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    date_of_birth = models.DateField()
    guardian = models.ForeignKey(Customer, on_delete=models.CASCADE)

    def __str__(self):
        """return the string representation of the dependent"""
        return f'{self.first_name} {self.last_name}'


class Employee(models.Model):
    """defines the employee model with its fields and methods"""

    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    is_manager = models.BooleanField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        """return the string representation of an employee"""
        return f'{self.first_name} {self.last_name}'


class Sale(models.Model):
    """defines the sale model with its fields and methods"""

    created_at = models.DateTimeField(auto_now_add=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    amount_paid = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        """return the string representation of a sale"""
        return f'{self.customer} on {self.created_at}'


class Item(models.Model):
    """defines the item model with its fields and methods"""

    name = models.CharField(max_length=128)
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        """return the string representation of an item"""
        return f'{self.name} (${self.price})'


class SaleItem(models.Model):
    """saleitem model to tie the sale and item tables"""

    sale = models.ForeignKey(Sale, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    description = models.TextField()

    def __str__(self):
        """return the string representation of saleitem"""
        return f'{self.item} to {self.sale}'