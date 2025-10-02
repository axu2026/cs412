# mini_insta/views.py
# Aidan Xu (axu26@bu.edu), 9/24/25
# The views code used for the mini_insta app

from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.views.generic import *
from .models import *
from .forms import *

# Create your views here.
class ProfileListView(ListView):
    """A view class to show all profiles"""

    model = Profile
    template_name = "mini_insta/show_all_profiles.html"
    context_object_name = "profiles" # all profiles


class ProfileDetailView(DetailView):
    """A view class to show more details of a single profile"""

    model = Profile
    template_name = "mini_insta/show_profile.html"
    context_object_name = "profile" # single profile


class PostDetailView(DetailView):
    """A view class to show more details of a single post"""

    model = Post
    template_name = "mini_insta/show_post.html"
    context_object_name = "post" # single post


class CreatePostView(CreateView):
    """A view to allow creation of a post with a form"""

    form_class = CreatePostForm
    template_name = "mini_insta/create_post_form.html"

    def get_context_data(self):
        """specifies context variables for the post create view"""

        # find the key of the profile, get the profile, then add it to the form
        context = super().get_context_data()
        pk = self.kwargs['pk']
        profile = Profile.objects.get(pk=pk)

        # add that profile to the context
        context['profile'] = profile

        return context

    def get_success_url(self):
        """redirects user to the profile view once a post is submitted"""
        pk = self.kwargs['pk']  # pk to the right profile
        return reverse('show_profile', kwargs={'pk':pk})

    def form_valid(self, form):
        """Handles form submission, used to add foreign key to the post"""

        # find the key of the profile, get the profile, then add it to the form
        pk = self.kwargs['pk']
        profile = Profile.objects.get(pk=pk)
        form.instance.profile = profile

        # save the post for creation of the image
        self.object = form.save()

        # create a new image model from the url and connect it to the post
        new_image = Photo.objects.create(post=self.object, image_url=self.request.POST['image_url'])

        # go ask the superclass method to do it with our modified form
        return super().form_valid(form)