from django.db import models
from django.urls import reverse

# Create your models here.
class Comment(models.Model):
    """comment model"""

    username = models.TextField(blank=True)
    text = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.username} at {self.timestamp}'
    
    def get_absolute_url(self):
        return reverse('comment', kwargs={'pk':self.pk})
    
    def get_all_replies(self):
        replies = Reply.objects.filter(comment=self)
        return replies


class Reply(models.Model):
    """reply model"""

    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    username = models.TextField(blank=True)
    text = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.username} at {self.timestamp}'