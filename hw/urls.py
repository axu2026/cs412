from django.urls import path
from django.conf import settings
from . import views
from .views import *

urlpatterns = [
    path('', CommentListView.as_view(), name="home"),
    path('comment/<int:pk>', CommentDetailView.as_view(), name="comment"),
    path('create', CommentCreateView.as_view(), name="create"),
    path('comment/<int:pk>/reply', ReplyCreateView.as_view(), name="create_reply")
]