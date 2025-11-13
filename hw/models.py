from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.
class Comment(models.Model):
    """comment model"""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now=True)
    image_url = models.URLField(blank=True)
    image_file = models.ImageField(blank=True)

    def __str__(self):
        return f'{self.user} at {self.timestamp}'
    
    def get_absolute_url(self):
        return reverse('comment', kwargs={'pk':self.pk})
    
    def get_all_replies(self):
        replies = Reply.objects.filter(comment=self)
        return replies


class Reply(models.Model):
    """reply model"""

    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now=True)
    image_url = models.URLField(blank=True)
    image_file = models.ImageField(blank=True)

    def __str__(self):
        return f'{self.user} at {self.timestamp}'
    

class UserStat(models.Model):
    name = models.TextField()
    age = models.IntegerField()
    gender = models.TextField()
    hours_online = models.FloatField()

    def __str__(self):
        return f'{self.name}, {self.age}'


def load_data():
    filename = 'practice.csv'
    f = open(filename, 'r')
    f.readline()

    for line in f:
        try:
            fields = line.strip().split(',')
            user = UserStat(name=fields[0],age=fields[1],gender=fields[2],hours_online=fields[3])
            user.save()
        except Exception as e:
            print(e)
            print(f'issue with line: {line}')