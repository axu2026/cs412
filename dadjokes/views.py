# dadjokes/views.py
# aidan xu (axu26@bu.edu) 11/11/2025
# the views defined for the dadjokes application

from django.shortcuts import render
from django.views.generic import *
from .models import *
from .serializers import *
from rest_framework import generics
import random

# Create your views here.
class RandomTemplateView(TemplateView):
    """view to display a random joke and picture"""

    template_name = "dadjokes/random.html"

    def get_context_data(self, **kwargs):
        """add a random joke and photo into the context"""
        context = super().get_context_data(**kwargs)

        # add a random joke into context
        joke_pks = Joke.objects.values_list('pk', flat=True)
        context['joke'] = Joke.objects.get(pk=random.choice(joke_pks))

        # add a random picture into context
        picture_pks = Picture.objects.values_list('pk', flat=True)
        context['picture'] = Picture.objects.get(pk=random.choice(picture_pks))

        return context
    

class JokeListView(ListView):
    """view to display a list of jokes"""

    model = Joke
    template_name = "dadjokes/joke_list.html"
    context_object_name = "jokes"


class JokeDetailView(DetailView):
    """view to display a single joke"""

    model = Joke
    template_name = "dadjokes/joke_detail.html"
    context_object_name = "joke"


class PictureListView(ListView):
    """view to display a list of pictures"""

    model = Picture
    template_name = "dadjokes/picture_list.html"
    context_object_name = "pictures"


class PictureDetailView(DetailView):
    """view to display a single picture"""

    model = Picture
    template_name = "dadjokes/picture_detail.html"
    context_object_name = "picture"


class JokeListAPIView(generics.ListCreateAPIView):
    """api view to list and create jokes"""

    queryset = Joke.objects.all()
    serializer_class = JokeSerializer


class PictureListAPIView(generics.ListAPIView):
    """api view to list pictures"""

    queryset = Picture.objects.all()
    serializer_class = PictureSerializer


class JokeAPIView(generics.RetrieveAPIView):
    """api view to retrieve a single joke"""

    queryset = Joke.objects.all()
    serializer_class = JokeSerializer


class PictureAPIView(generics.RetrieveAPIView):
    """api view to retrieve a single picture"""

    queryset = Picture.objects.all()
    serializer_class = PictureSerializer


class RandomAPIView(generics.RetrieveAPIView):
    """api view to retrieve a random joke"""

    queryset = Joke.objects.all()
    serializer_class = JokeSerializer

    def get_object(self):
        """return a random joke object"""

        joke_pks = Joke.objects.values_list('pk', flat=True)
        random_pk = random.choice(joke_pks)

        return Joke.objects.get(pk=random_pk)