from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.views.generic import *
from .models import *
from .forms import *

import time
import random

# Create your views here.
class CommentListView(ListView):
    """return the view for the list of comments"""

    model = Comment
    template_name = "hw/home.html"
    context_object_name = "comments"


class CommentDetailView(DetailView):
    """return the view for a specific comment"""

    model = Comment
    template_name = "hw/comment.html"
    context_object_name = "comment"


class CommentCreateView(CreateView):
    """return the view for creating a comment"""

    form_class = CreateCommentForm
    template_name = "hw/create_comment.html"

class ReplyCreateView(CreateView):
    """make a reply"""

    form_class = CreateReplyForm
    template_name = "hw/create_reply.html"

    def get_context_data(self):
        context = super().get_context_data()
        pk = self.kwargs['pk']
        comment = Comment.objects.get(pk=pk)
        context['comment'] = comment

        return context
    
    def form_valid(self, form):
        pk = self.kwargs['pk']
        comment = Comment.objects.get(pk=pk)
        form.instance.comment = comment

        return super().form_valid(form)
    
    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse('comment', kwargs={'pk':pk})
    
class CommentUpdateView(UpdateView):
    """update a comment"""

    model = Comment
    form_class = UpdateCommentForm
    template_name = "hw/update_comment.html"

class ReplyUpdateView(UpdateView):
    model = Reply
    form_class = UpdateReplyForm
    template_name = "hw/update_reply.html"

    def get_success_url(self):
        reply = Reply.objects.get(pk=self.kwargs['pk'])
        return reverse('comment', kwargs={'pk':reply.comment.pk})
    
class CommentDeleteView(DeleteView):
    model = Comment
    template_name = "hw/delete_comment.html"

    def get_success_url(self):
        return reverse('home')
    
class ReplyDeleteView(DeleteView):
    model = Reply
    template_name = "hw/delete_reply.html"

    def get_success_url(self):
        pk = self.kwargs['pk']
        reply = Reply.objects.get(pk=pk)
        comment = reply.comment

        return reverse('comment', kwargs={'pk': comment.pk})