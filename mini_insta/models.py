# mini_insta/models.py
# Aidan Xu (axu26@bu.edu), 9/24/25
# used to define data models for the mini_insta app

from django.db import models
from django.urls import reverse

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
    
    def get_absolute_url(self):
        """returns the url to an instance of a profile"""
        return reverse('show_profile', kwargs={'pk':self.pk})
    

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
        return f'{self.profile} at {self.timestamp}'

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
            # check if theres a url first
            if first_photo.image_url:
                return first_photo.image_url

            # if its not a url check for a file and return
            if first_photo.image_file:
                return first_photo.image_file.url
        
        # else we return the path to the no image default
        return "../../static/no_image.png"
    
    def get_absolute_url(self):
        """returns the url to an instance of a post"""
        return reverse('show_post', kwargs={'pk':self.pk})


class Photo(models.Model):
    """class representing the data for a photo attached to a post"""

    # foreign key connecting this photo to a post instance
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    # the url for the image
    image_url = models.URLField(blank=True)

    # the date the photo was uploaded to the site
    timestamp = models.DateTimeField(auto_now=True)

    # new image file field
    image_file = models.ImageField(blank=True)

    def __str__(self):
        """the string representation for the photo"""
        # if theres a url, use the url for the string
        if self.image_url:
            return f'{self.image_url} on {self.timestamp}'
        
        # if theres an image file instead, use the file name for the string
        if self.image_file:
            return f'{self.image_file} on {self.timestamp}'

        # in case theres no image info
        return f'no image on {self.timestamp}'
    
    def get_image_url(self):
        """returns the url of the image"""
        # if theres a url return it
        if self.image_url:
            return self.image_url
        
        # if theres an image file return the url for it
        if self.image_file:
            return self.image_file.url
        
        return None # incase of neither