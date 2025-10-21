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


class UpdatePostForm(forms.ModelForm):
    """The form to update a post"""

    class Meta:
        """ties the form to the post model"""
        model = Post
        fields = ['caption']

    
class CreateProfileForm(forms.ModelForm):
    """The form to create a new profile"""

    class Meta:
        """ties the form to the profile model"""
        model = Profile
        fields = ['display_name', 'bio_text', 'profile_image_url']


class CreateFollowForm(forms.ModelForm):
    """A form, but not really, used to make a follow"""

    class Meta:
        """No fields, we will assign frields programatically"""
        model = Follow
        fields = []


class CreateLikeForm(forms.ModelForm):
    """A form, but not really, used to make a like"""

    class Meta:
        """No fields, we will assign frields programatically"""
        model = Like
        fields = []


class CreateCommentForm(forms.ModelForm):
    """A form to create a comment on a post"""

    class Meta:
        """link the fields to the comment model"""
        model = Comment
        fields = ['text']