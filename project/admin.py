# project/admin.py
# Aidan Xu (axu26@bu.edu) 11/23/25
# registers all models to the admin interface for creation and updating

from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Customer)
admin.site.register(Dependent)
admin.site.register(Employee)
admin.site.register(Sale)
admin.site.register(Item)
admin.site.register(SaleItem)