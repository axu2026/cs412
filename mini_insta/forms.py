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


class UpdateProfileForm(forms.ModelForm):
    """The form to update a profile"""

    class Meta:
        """ties the form to the profile model"""
        model = Profile
        fields = ['profile_image_url', 'display_name', 'bio_text']