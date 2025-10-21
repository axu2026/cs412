from django import forms
from .models import *

class CreateCommentForm(forms.ModelForm):
    """the form to create a new comment"""

    class Meta:
        """field for the form"""
        model = Comment
        fields = ['username', 'text', 'image_url', 'image_file']


class CreateReplyForm(forms.ModelForm):
    """the form to create a new reply"""

    class Meta:
        """field for the form"""
        model = Reply
        fields = ['username', 'text', 'image_url', 'image_file']

class UpdateCommentForm(forms.ModelForm):
    """updates the comment object"""

    class Meta:
        model = Comment
        fields = ['text', 'image_url', 'image_file']

class UpdateReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ['text', 'image_url', 'image_file']