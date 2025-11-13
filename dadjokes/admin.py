# dadjokes/admin.py
# aidan xu (axu26@bu.edu) 11/11/2025
# register the models to the admin page

from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Joke)
admin.site.register(Picture)