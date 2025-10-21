from django.urls import path
from django.conf import settings
from . import views
from .views import *

urlpatterns = [
    path('', CommentListView.as_view(), name="home"),
    path('comment/<int:pk>', CommentDetailView.as_view(), name="comment"),
    path('create', CommentCreateView.as_view(), name="create"),
    path('comment/<int:pk>/reply', ReplyCreateView.as_view(), name="create_reply"),
    path('comment/<int:pk>/update', CommentUpdateView.as_view(), name="update_comment"),
    path('reply/<int:pk>/update', ReplyUpdateView.as_view(), name="update_reply"),
    path('comment/<int:pk>/delete', CommentDeleteView.as_view(), name="delete_comment"),
    path('reply/<int:pk>/delete', ReplyDeleteView.as_view(), name="delete_reply"),
]