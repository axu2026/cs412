# mini_insta/models.py
# Aidan Xu (axu26@bu.edu), 9/24/25
# used to define data models for the mini_insta app

from django.db import models

# Create your models here.
class Profile(models.Model):
    """The data representing an account within the mini insta app"""

    # the log-in name prefix with an @ in the app
    username = models.TextField(blank=True)

    # the main name displayed in the app
    display_name = models.TextField(blank=True)

    # the url for the profile picture
    profile_image_url = models.URLField(blank=True)

    # the bio to be displayed in the detailed profile view
    bio_text = models.TextField(blank=True)

    # the time when the account was made displayed in detailed view
    join_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        """String representation of the profile model"""
        return f'{self.username}'