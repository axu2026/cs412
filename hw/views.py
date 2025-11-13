from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.views.generic import *
from .models import *
from .forms import *

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

import plotly
import plotly.graph_objs as go

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

    def get_login_url(self):
        return reverse('loginhw')


class CommentCreateView(LoginRequiredMixin, CreateView):
    """return the view for creating a comment"""

    form_class = CreateCommentForm
    template_name = "hw/create_comment.html"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
    def get_login_url(self):
        return reverse('loginhw')

class ReplyCreateView(LoginRequiredMixin, CreateView):
    """make a reply"""

    form_class = CreateReplyForm
    template_name = "hw/create_reply.html"

    def get_context_data(self):
        context = super().get_context_data()
        pk = self.kwargs['pk']
        comment = Comment.objects.get(pk=pk)
        context['comment'] = comment

        return context
    
    def get_login_url(self):
        return reverse('loginhw')
    
    def form_valid(self, form):
        pk = self.kwargs['pk']
        comment = Comment.objects.get(pk=pk)
        form.instance.comment = comment
        form.instance.user = self.request.user

        return super().form_valid(form)
    
    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse('comment', kwargs={'pk':pk})
    
class CommentUpdateView(LoginRequiredMixin, UpdateView):
    """update a comment"""

    model = Comment
    form_class = UpdateCommentForm
    template_name = "hw/update_comment.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            comment = Comment.objects.get(pk=self.kwargs['pk'])
            if comment.user != request.user:
                return render(request, "hw/no.html")
        
        return super().dispatch(request, *args, **kwargs)

    def get_login_url(self):
        return reverse('loginhw')

class ReplyUpdateView(LoginRequiredMixin, UpdateView):
    model = Reply
    form_class = UpdateReplyForm
    template_name = "hw/update_reply.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            reply = Reply.objects.get(pk=self.kwargs['pk'])
            if reply.user != request.user:
                return render(request, "hw/no.html")
        
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        reply = Reply.objects.get(pk=self.kwargs['pk'])
        return reverse('comment', kwargs={'pk':reply.comment.pk})
    
    def get_login_url(self):
        return reverse('loginhw')
    
class CommentDeleteView(LoginRequiredMixin, DeleteView):
    model = Comment
    template_name = "hw/delete_comment.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            comment = Comment.objects.get(pk=self.kwargs['pk'])
            if comment.user != request.user:
                return render(request, "hw/no.html")
        
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('home')
    
    def get_login_url(self):
        return reverse('loginhw')
    
class ReplyDeleteView(LoginRequiredMixin, DeleteView):
    model = Reply
    template_name = "hw/delete_reply.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            reply = Reply.objects.get(pk=self.kwargs['pk'])
            if reply.user != request.user:
                return render(request, "hw/no.html")
        
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        pk = self.kwargs['pk']
        reply = Reply.objects.get(pk=pk)
        comment = reply.comment

        return reverse('comment', kwargs={'pk': comment.pk})
    
    def get_login_url(self):
        return reverse('loginhw')
    
class UserRegistrationView(CreateView):
    template_name = "hw/signup.html"
    form_class = UserCreationForm
    model = User

    def get_success_url(self):
        
        return reverse('home')
    

class StatListView(ListView):
    model = UserStat
    template_name = "hw/stats.html"
    context_object_name = "stats"
    paginate_by = 5

    def get_queryset(self):
        qs = super().get_queryset()

        if 'gender' in self.request.GET and self.request.GET['gender']:
            qs = qs.filter(gender=self.request.GET['gender'])

        return qs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        qs = self.get_queryset()

        x = ['Male', 'Female']
        y = [qs.filter(gender="Male").count(),qs.filter(gender="Female").count()]

        fig = go.Bar(x=x, y=y)
        graph = plotly.offline.plot({"data":[fig],
                                     "layout_title_text":"gender of users"},
                                     auto_open=False,
                                     output_type="div")
        
        context['graph'] = graph

        return context