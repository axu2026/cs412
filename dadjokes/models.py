# dadjokes/models.py
# aidan xu (axu26@bu.edu) 11/11/2025
# defines the models for the dadjokes application

from django.db import models

# Create your models here.
class Joke(models.Model):
    """the joke model and its fields"""

    joke = models.TextField()
    contributor = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """returns the string representation of the joke model"""
        return f'joke by {self.contributor} on {self.timestamp}'
    

class Picture(models.Model):
    """the picture model storing joke photo/gif data"""

    image_url = models.URLField()
    contributor = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """return string representation of the picture model"""
        return f'image by {self.contributor} on {self.timestamp}'