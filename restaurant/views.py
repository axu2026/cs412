# restaurant/views.py
# Aidan Xu (axu26@bu.edu), 9/16/25
# The views code used for the restaurant app

from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

import time
import random

# dictionary holding all foods and their prices
menu = {
    "Egg Rolls": 2.95,
    "Fried Rice": 6.50,
    "Lo Mein": 10.25,
    "General Tso's Chicken": 13.25,
    "Chow Mein": 9.75,
    "Chicken Broccoli": 11.25,
    "Spare Ribs": 11.25,
    "Kung Pao Chicken": 11.25,
}

# dictionary holding all fried rice types and their prices
fried_rice = {
    "Plain": 0.0,
    "Vegetable": 1.0,
    "Pork": 1.5,
}

# list holding all possible daily special foods. will be picked from randomly
specials = [
    "Chow Mein",
    "Chicken Broccoli",
    "Spare Ribs",
    "Kung Pao Chicken",
]

# not essential but for fun calculations at confirmation page
tax_rate = 0.07

# Create your views here.
def main(request):
    """Handles and sends the base page for the restaurant app"""
    
    template_name = "restaurant/main.html"
    context = {
        "time": time.ctime(),
    }

    return render(request, template_name, context)

def order(request):
    """Handles the order request by providing a form"""

    # randomly pick the daily special from the specials list
    special = random.choice(specials)

    template_name = "restaurant/order.html"
    context = {
        "time": time.ctime(),
        "special": special,
        "special_price": menu[special], # get price of special too
    }

    return render(request, template_name, context)

def confirmation(request):
    """Handles the confirmation page when an order is submitted"""

    template_name = "restaurant/confirmation.html"
    context = {
        "time": time.ctime(),
    }

    print(request.POST)

    if request.POST:
        # the price of the order, will be summed up
        price = 0.0

        # retrieving customer information
        name = request.POST['name']
        phone = request.POST['phone']
        email = request.POST['email']

        # retrieve special instructions
        special_instructions = request.POST['special_instructions']

        # list of food items and prices used to display what the customer ordered
        items = []

        # iterate through the post, add items to the order list and add up price
        for key, _ in request.POST.items():
            # in case a weird tag gets through, check if key is in menu
            if key in menu:
                item_price = menu[key]

                # for fried rice, chekc for which type of rice it is
                prefix = "" # empty for any other item
                if key == "Fried Rice":
                    prefix = request.POST['fried_rice_type']# get the type here
                    price += fried_rice[prefix]            # add to total price
                    item_price += fried_rice[prefix]      # adjust price display
                    prefix = prefix + " " # makes a space when displaying item

                # append key with price, format price to have 2 decimals
                items.append(prefix + key + " $" + "{:.2f}".format(item_price))
                price += menu[key]

        # a fun calculation to include, calculates sales tax
        tax = price * tax_rate

        # calculate the total price with the tax
        total = price + tax

        # the time the order will be ready, 30-60 minutes after placing order
        ready_time = time.ctime(time.time() + random.randint(30, 60) * 60)

        context = {
            "time": time.ctime(),
            "name": name,
            "phone": phone,
            "email": email,
            "special_instructions": special_instructions,
            "price": "{:.2f}".format(price), # format to always show 2 decimals
            "tax": "{:.2f}".format(tax),     #
            "total": "{:.2f}".format(total), #
            "items": items,
            "ready_time": ready_time,
        }

    return render(request, template_name, context)