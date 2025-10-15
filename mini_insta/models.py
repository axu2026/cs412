# mini_insta/models.py
# Aidan Xu (axu26@bu.edu), 9/24/25
# used to define data models for the mini_insta app

from django.db import models
from django.urls import reverse
import random

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
    
    def get_followers(self):
        """returns the list of profiles following this profile"""
        result = [] # the actual return result of profiles
        follows = Follow.objects.filter(profile=self)

        # iterate through the list of follows and append follower to result list
        for follow in follows:
            result.append(follow.follower_profile)

        return result
    
    def get_num_followers(self):
        """returns the number of followers a profile has"""
        return Follow.objects.filter(profile=self).count()
    
    def get_following(self):
        """returns the list of profiles that the profile follows"""
        result = [] # the actual return result of profiles
        follows = Follow.objects.filter(follower_profile=self)

        # iterate through the list of follows and append profile to result list
        for follow in follows:
            result.append(follow.profile)

        return result

    def get_num_following(self):
        """return the number of profiles the user follows"""
        return Follow.objects.filter(follower_profile=self).count()
    
    def get_post_feed(self):
        """returns a list of posts from the user's following"""
        followed = self.get_following() # get followers of the profile
        result = []                     # store all posts here

        # go through all followers and add their posts to feed
        for follow in followed:
            posts = Post.objects.filter(profile=follow)
            # append these posts to the result
            for post in posts:
                result.append(post)

        # shuffle the result so that the feed is more varied
        random.shuffle(result)

        return result
    

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
    
    def can_show_photo_feed(self):
        """check if a photo can be shown on a feed"""

        # if there is no photo
        if Photo.objects.filter(post=self).count() <= 0:
            return False
        
        return True
    
    def get_absolute_url(self):
        """returns the url to an instance of a post"""
        return reverse('show_post', kwargs={'pk':self.pk})
    
    def get_all_comments(self):
        """returns all comments for this post"""
        comments = Comment.objects.filter(post=self)
        return comments
    
    def get_comment_count(self):
        """returns number of comments for a post"""
        return Comment.objects.filter(post=self).count()

    def get_comments_left_feed(self):
        """for the feed, returns number of comments left"""
        count = self.get_comment_count() - 3 # get amount

        # case for 1 or multiple left
        if count == 1:
            return 'and 1 more comment...'
        elif count > 1:
            return f'and {count} more comments'
        
        # no additional comments
        return ""


    def get_likes(self):
        """returns the likes from the post"""
        likes = Like.objects.filter(post=self)
        return likes
    
    def get_like_count(self):
        """return the number of likes a post has"""
        return Like.objects.filter(post=self).count()
    
    def get_example_likers(self):
        """return a string of who may be liking a post"""
        count = self.get_like_count()
        
        # cases for which strings to return
        if count == 0:
            # no likes
            return 'likes'
        elif count == 1:
            # only one like, get the liker
            like = self.get_likes().first()
            return f'like by @{like.profile}'
        else:
            # multiple likers, return an example liker and count of others
            like = self.get_likes().first()
            others = count - 1
            end_word = "others"

            # adjusting grammar of the statement accordingly
            if others == 1:
                end_word = "other"

            return f'likes by @{like.profile} and {others} {end_word}'
        
    def get_first_few_comments(self):
        """obtain the first few comments to be displayed in feed"""
        result = []
        comments = Comment.objects.filter(post=self)

        # go through comments
        for comment in comments:
            result.append(comment) # add comment to result list

            # after getting 3, stop getting anymore
            if len(result) > 2:
                break

        return result
            

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
    

class Follow(models.Model):
    """class representing the follow linking two profiles together"""

    # the following profile
    follower_profile = models.ForeignKey(Profile, 
                                         on_delete=models.CASCADE, 
                                         related_name="follower_profile")
    
    # the profile being followed
    profile = models.ForeignKey(Profile, 
                                on_delete=models.CASCADE, 
                                related_name="profile")
    
    # the date when follower started following
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        """return the string representation of the follow"""
        return f'{self.follower_profile} is following {self.profile}'
    

class Comment(models.Model):
    """class representing a comment on a post"""

    # the foreign key to the post the comment is on
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    # the foreign key to the profile making the comment
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    # the time the comment was created
    timestamp = models.DateTimeField(auto_now=True)

    # the text field for the comment
    text = models.TextField(blank=True)

    def __str__(self):
        """returns a string representation of a comment"""
        return f'{self.profile}\'s comment on {self.timestamp}'
    

class Like(models.Model):
    """class representing a like on a post from a profile"""

    # foreign key of the post that the like is on
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    # the foreign key of the profile doing the like
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    # the time the like was created
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        """string representation of the like"""
        return f'{self.profile} liked {self.post}'