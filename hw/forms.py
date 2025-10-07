from django import forms
from .models import *

class CreateCommentForm(forms.ModelForm):
    """the form to create a new comment"""

    class Meta:
        """field for the form"""
        model = Comment
        fields = ['username', 'text']


class CreateReplyForm(forms.ModelForm):
    """the form to create a new reply"""

    class Meta:
        """field for the form"""
        model = Reply
        fields = ['username', 'text']