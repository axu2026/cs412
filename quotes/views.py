# views.py
# Aidan Xu (axu26@bu.edu), 9/9/25
# The views code used for the quotes app

from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

import random
import time

# the list of quotes used for the quotes app
quotes = [
    "Sometimes it's a form of love just to talk to somebody that you have nothing in common with and still be fascinated by their presence.",
    "Things fall apart, it's scientific.",
    "The less we say about it the better, make it up as we go along.",
    "If your work isn't what you love, then something isn't right.",
    "To some extent I happily don't know what I'm doing. I feel that it's an artist's responsibility to trust that.",
    "Life tends to be an accumulation of a lot of mundane decisions, which often gets ignored.",
    "I felt like a bit of an outsider. But then I realized the world was made up of people who were all different. But we're all here."
]

# the list of urls for images
images = [
    "https://images.squarespace-cdn.com/content/v1/528809f3e4b0a1b235b315c6/1581020458277-AILUY4BM7SV08X50E0WJ/DAVIDBYRNE.jpg",
    "https://media.newyorker.com/photos/6509c266df6f169a2b0e1448/1:1/w_1501,h_1501,c_limit/Brody-SMS_005.jpg",
    "https://i0.wp.com/bamfstyle.com/wp-content/uploads/2024/10/SMSBigSuit-MAIN1.jpg",
    "https://images.squarespace-cdn.com/content/v1/5843057debbd1a9265704e03/0cd8c28f-c92e-42ea-bc79-bc95e7e7a11c/Youngbyrne.jpeg",
    "https://guitar.com/wp-content/uploads/2021/12/Talking-Heads-David-Byrne-Credit-Chris-Walter-WireImage@1050x1400.jpg",
]

# Create your views here.
def quote(request):
    """Handles request for quote page by returning a random image and quote"""

    template_name = "quotes/quote.html"
    context = {
        "quote": random.choice(quotes),
        "image": random.choice(images),
        "time": time.ctime(),
    }
    
    return render(request, template_name, context)

def show_all(request):
    """Handles request for show all page by showing all photos and quotes"""

    template_name = "quotes/show_all.html"
    context = {
        "quotes": quotes,
        "images": images,
        "time": time.ctime(),
    }

    return render(request, template_name, context)

def about(request):
    """Handles request for about page by returning information of the figure"""

    template_name = "quotes/about.html"
    context = {
        "time": time.ctime(),
    }

    return render(request, template_name, context)