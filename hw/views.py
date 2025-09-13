from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

import time
import random

# Create your views here.
def home(request):
    """The hello world home page request"""

    response_text = f"""
    <html>
    <h1>Hello, world!</h1>
    It is currently {time.ctime()}
    </html>
    """

    return HttpResponse(response_text)

def home_page(request):
    template_name = "hw/home.html"
    context = {
        "time": time.ctime(),
        "a": random.randint(0,10),
        "b": random.randint(0,10),
    }
    return render(request, template_name, context)