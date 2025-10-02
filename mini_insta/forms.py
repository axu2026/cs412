# mini_insta/forms.py
# Aidan Xu (axu26@bu.edu), 10/1/25
# file that creates the forms so we can make new posts in our app

from django import forms
from .models import *

class CreatePostForm(forms.ModelForm):
    """The form to create a new post"""

    class Meta:
        """ties this form to the post model"""
        model = Post
        fields = ['caption']