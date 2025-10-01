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
    
    def get_all_posts(self):
        """returns a queryset of all posts from a profile"""
        posts = Post.objects.filter(profile=self)
        return posts
    
    def get_posts_count(self):
        """returns the amount of posts attributed to a profile"""
        return Post.objects.filter(profile=self).count()
    

class Post(models.Model):
    """class representing the data for posts that users can make"""

    # the foreign key connecting the post to a specific author/profile
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    # the text content of the post
    caption = models.TextField(blank=True)

    # the date that the post was created on
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        """the string representation of the post"""
        return f'{self.caption}'

    def get_all_photos(self):
        """returns the queryset of all photos from a post"""
        photos = Photo.objects.filter(post=self)
        return photos
    
    def get_first_photo(self):
        """returns the url of the first associated image (if present)"""
        # obtain all photos and then grab the first
        photos = Photo.objects.filter(post=self)
        first_photo = photos.first()

        # check if that photo exists first before returning its url
        if first_photo:
            return first_photo.image_url
        
        # else we return the path to the no image default
        return "../../static/no_image.png"


class Photo(models.Model):
    """class representing the data for a photo attached to a post"""

    # foreign key connecting this photo to a post instance
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    # the url for the image
    image_url = models.URLField(blank=True)

    # the date the photo was uploaded to the site
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        """the string representation for the photo"""
        return f'{self.image_url}'