# mini_insta/views.py
# Aidan Xu (axu26@bu.edu), 9/24/25
# The views code used for the mini_insta app

from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.views.generic import *
from .models import *
from .forms import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import login

# Create your views here.
class ProfileListView(ListView):
    """A view class to show all profiles"""

    model = Profile
    template_name = "mini_insta/show_all_profiles.html"
    context_object_name = "profiles" # all profiles


class ProfileDetailView(DetailView):
    """A view class to show more details of a single profile"""

    model = Profile
    template_name = "mini_insta/show_profile.html"

    def get_context_data(self, **kwargs):
        """override the context data for dealing with follow button"""
        context = super().get_context_data(**kwargs)

        # get the profile and add it to the context
        pk = self.kwargs['pk']
        profile = Profile.objects.get(pk=pk)
        context['profile'] = profile

        # if there is a user, check if there is already a follow
        if self.request.user.is_authenticated:
            user = self.request.user
            user_profile = Profile.objects.get(user=user)
            context['already_followed'] = Follow.objects.filter(follower_profile=user_profile,
                                                            profile=profile)
        else:
            context['already_followed'] = None # otherwise there is no follow

        return context


class PostDetailView(DetailView):
    """A view class to show more details of a single post"""

    model = Post
    template_name = "mini_insta/show_post.html"

    def get_context_data(self, **kwargs):
        """specifies context variables for the post detail view"""
        context = super().get_context_data(**kwargs)
        pk = self.kwargs['pk']
        post = Post.objects.get(pk=pk)
        context['post'] = post

        # check for user, if there is one, then there may already be a like
        if self.request.user.is_authenticated:
            user = self.request.user
            user_profile = Profile.objects.get(user=user)
            like = Like.objects.filter(post=post, profile=user_profile)

            context['liked'] = like
        else:
            context['liked'] = None

        return context


class CreatePostView(LoginRequiredMixin, CreateView):
    """A view to allow creation of a post with a form"""

    form_class = CreatePostForm
    template_name = "mini_insta/create_post_form.html"

    def get_login_url(self):
        """return the log in url for when a non-user tries to create a post"""
        return reverse('login')
    
    def get_object(self, queryset=None):
        """return the right profile object according to the current user"""
        return Profile.objects.get(user=self.request.user)

    def get_context_data(self):
        """specifies context variables for the post create view"""

        # get the context
        context = super().get_context_data()

        # add that profile to the context using get_object()
        context['profile'] = self.get_object()

        return context

    # commented out since instructions is to show post after making the post
    # will automatically use get_absolute_url from post model
    """
    def get_success_url(self):
        #redirects user to the profile view once a post is submitted
        pk = self.kwargs['pk']  # pk to the right profile
        return reverse('show_profile', kwargs={'pk':pk})
    """

    def form_valid(self, form):
        """Handles form submission, used to add foreign key to the post"""

        # fill in the profile field of the form
        form.instance.profile = self.get_object()

        # save the post for creation of the image
        self.object = form.save()

        # create a new image model from the url and connect it to the post
        #new_image = Photo.objects.create(post=self.object, image_url=self.request.POST['image_url'])

        files = self.request.FILES.getlist('images')

        # go through all files and create the photo records for them
        for file in files:
            Photo.objects.create(post=self.object, image_file=file)

        # go ask the superclass method to do it with our modified form
        return super().form_valid(form)


class UpdateProfileView(LoginRequiredMixin, UpdateView):
    """A view to update a profile with a form"""

    form_class = UpdateProfileForm
    template_name = "mini_insta/update_profile_form.html"
    model = Profile

    def get_login_url(self):
        """return url for login if not logged in"""
        return reverse('login')
    
    def get_object(self, queryset = None):
        """return the right profile object according to the current user"""
        return Profile.objects.get(user=self.request.user)

    def get_context_data(self, **kwargs):
        """change context to include profile"""
        
        context = super().get_context_data(**kwargs)

        user = self.request.user                 # get the user
        profile = Profile.objects.get(user=user) # find profile of the user

        context['profile'] = profile

        return context
        

class DeletePostView(LoginRequiredMixin, DeleteView):
    """A view to prompt the user to delete a post"""

    template_name = "mini_insta/delete_post_form.html"
    model = Post

    def dispatch(self, request, *args, **kwargs):
        """override to check if the user has permission to do this action"""
        pk = self.kwargs['pk']          # get the post pk
        post = Post.objects.get(pk=pk)  # get the post

        # check if there is currently a user, and if that user is/isnt the poster
        if request.user.is_authenticated and request.user != post.profile.user:
            # the user is not the poster, and is denied permission
            return render(request, "mini_insta/permission_denied.html")

        # send the delete page
        return super().dispatch(request, *args, **kwargs)

    def get_login_url(self):
        """return url for login if not logged in"""
        return reverse('login')

    def get_success_url(self):
        """return url back to the profile that the delete post came from"""
        
        pk = self.kwargs['pk']         # access the post to access the profile
        post = Post.objects.get(pk=pk) # get post object
        profile = post.profile         # the profile object

        return reverse('show_profile', kwargs={'pk': profile.pk})

    def get_context_data(self, **kwargs):
        """override for the context data"""

        context = super().get_context_data(**kwargs)
        pk = self.kwargs['pk']          # the post pk
        post = Post.objects.get(pk=pk)
        profile = post.profile          # find the profile from post

        # add both to context
        context['post'] = post
        context['profile'] = profile

        return context


class UpdatePostView(LoginRequiredMixin, UpdateView):
    """A view to update a post"""

    form_class = UpdatePostForm
    template_name = "mini_insta/update_post_form.html"
    model = Post

    def dispatch(self, request, *args, **kwargs):
        """override to check if the user has permission to do this action"""
        pk = self.kwargs['pk']          # get the post pk
        post = Post.objects.get(pk=pk)  # get the post

        # check if there is currently a user, and if that user is/isnt the poster
        if request.user.is_authenticated and request.user != post.profile.user:
            # the user is not the poster, and is denied permission
            return render(request, "mini_insta/permission_denied.html")

        # send the delete page
        return super().dispatch(request, *args, **kwargs)

    def get_login_url(self):
        """return url for login if not logged in"""
        return reverse('login')

    def get_context_data(self):
        """specifies context variables for the post update view"""

        # find the key of the post, get the post, get the profile
        context = super().get_context_data()
        pk = self.kwargs['pk']
        post = Post.objects.get(pk=pk)
        profile = post.profile

        # add that profile to the context
        context['profile'] = profile

        return context
    
    def form_valid(self, form):
        """Handles form submission to add additional photos"""

        # get files uploaded by the form
        files = self.request.FILES.getlist('images')

        # find the post object to save to the new photo's foreign key
        pk = self.kwargs['pk']
        post = Post.objects.get(pk=pk)

        # go through all files and create the photo records for them
        for file in files:
            Photo.objects.create(post=post, image_file=file)

        # go ask the superclass method to do it with our modified form
        return super().form_valid(form)
    

class DeletePhotoView(LoginRequiredMixin, DeleteView):
    """View to confirm deletion of a photo"""

    template_name = "mini_insta/delete_photo_form.html"
    model = Photo

    def dispatch(self, request, *args, **kwargs):
        """override to check if the user has permission to do this action"""
        pk = self.kwargs['pk']            # get the photo pk
        photo = Photo.objects.get(pk=pk)  # get the photo

        # check if there is currently a user, and if that user is/isnt the poster
        if request.user.is_authenticated and request.user != photo.post.profile.user:
            # the user is not the poster, and is denied permission
            return render(request, "mini_insta/permission_denied.html")

        # send the delete page
        return super().dispatch(request, *args, **kwargs)

    def get_login_url(self):
        """return url for login if not logged in"""
        return reverse('login')

    def get_context_data(self, **kwargs):
        """override for the context data"""

        context = super().get_context_data(**kwargs)
        pk = self.kwargs['pk']          # find photo with pk
        photo = Photo.objects.get(pk=pk)

        # add to context
        context['photo'] = photo

        return context
    
    def get_success_url(self):
        """return the url after successfully deleting photo"""
        
        pk = self.kwargs['pk']
        photo = Photo.objects.get(pk=pk)
        post = photo.post   # take back to the post after deletion

        return reverse('show_post', kwargs={'pk': post.pk})
    

class ShowFollowersDetailView(DetailView):
    """view showing all a profile's followers"""

    model = Profile
    template_name = "mini_insta/show_followers.html"
    context_object_name = "profile"

    def get_context_data(self, **kwargs):
        """override the context data for dealing with follow button"""
        context = super().get_context_data(**kwargs)

        # get the profile and add it to the context
        pk = self.kwargs['pk']
        profile = Profile.objects.get(pk=pk)
        context['profile'] = profile

        # if there is a user, check if there is already a follow
        if self.request.user.is_authenticated:
            user = self.request.user
            user_profile = Profile.objects.get(user=user)
            context['already_followed'] = Follow.objects.filter(follower_profile=user_profile,
                                                            profile=profile)
        else:
            context['already_followed'] = None # otherwise there is no follow

        return context


class ShowFollowingDetailView(DetailView):
    """view showing all a profile's follows"""

    model = Profile
    template_name = "mini_insta/show_following.html"
    context_object_name = "profile"

    def get_context_data(self, **kwargs):
        """override the context data for dealing with follow button"""
        context = super().get_context_data(**kwargs)

        # get the profile and add it to the context
        pk = self.kwargs['pk']
        profile = Profile.objects.get(pk=pk)
        context['profile'] = profile

        # if there is a user, check if there is already a follow
        if self.request.user.is_authenticated:
            user = self.request.user
            user_profile = Profile.objects.get(user=user)
            context['already_followed'] = Follow.objects.filter(follower_profile=user_profile,
                                                            profile=profile)
        else:
            context['already_followed'] = None # otherwise there is no follow

        return context


class PostFeedListView(LoginRequiredMixin, ListView):
    """view showing all posts for a user's feed"""

    model = Post
    template_name = "mini_insta/show_feed.html"
    context_object_name = "posts" # all posts

    def get_login_url(self):
        """return url for login if not logged in"""
        return reverse('login')

    def get_object(self, queryset=None):
        """return the right profile object according to the current user"""
        return Profile.objects.get(user=self.request.user)

    def get_context_data(self):
        """specifies context variables for feed"""

        # find the profile object and aff to context
        context = super().get_context_data()
        profile = self.get_object()

        # add that profile to the context
        context['profile'] = profile

        return context
    

class SearchView(LoginRequiredMixin, ListView):
    """view that gives the user a search bar to find posts/profiles"""

    template_name = "mini_insta/search_results.html"

    def get_login_url(self):
        """return url for login if not logged in"""
        return reverse('login')

    def dispatch(self, request, *args, **kwargs):
        """override the superclass dispatch method"""

        # if there is no query made yet, send the search form
        if not 'query' in self.request.GET and request.user.is_authenticated:
            # find profile of the user making search and put it into context
            user = self.request.user
            profile = Profile.objects.get(user=user)
            context = {
                "profile": profile,
            }
            return render(request, "mini_insta/search.html", context)

        # else show the results of query (or log in screen)
        return super().dispatch(request, *args, **kwargs)
    
    def get_queryset(self):
        """returns a queryset of posts based on the query"""
        query = self.request.GET['query']

        # get the query set of posts from the caption
        qs_caption = Post.objects.filter(caption__contains=query)

        return qs_caption

    def get_context_data(self, **kwargs):
        """specifies context variables for search"""

        # get user, then find profile with the user
        context = super().get_context_data(**kwargs)
        user = self.request.user
        profile = Profile.objects.get(user=user)

        # add that profile that is searching to the context
        context['profile'] = profile

        # if there is a query, then return the search query
        if 'query' in self.request.GET:
            query = self.request.GET['query']

            # for profile query sets, union them to avoid duplciates
            profiles_username = Profile.objects.filter(username__contains=query)
            profiles_display = Profile.objects.filter(display_name__contains=query)
            profiles_bio = Profile.objects.filter(bio_text__contains=query)
            profiles = profiles_username.union(profiles_display).union(profiles_bio)

            # for post query sets
            posts = self.get_queryset()

            # add them to the context
            context['profiles'] = profiles
            context['posts'] = posts
            context['query'] = query

        return context
    

class LoggedOutView(TemplateView):
    """log out confirmation view"""
    template_name = "mini_insta/logged_out.html"


class CreateProfileView(CreateView):
    """view to show a form to create a profile"""

    form_class = CreateProfileForm
    template_name = "mini_insta/create_profile_form.html"

    def get_context_data(self, **kwargs):
        """override the context method"""

        # get the original context
        context = super().get_context_data(**kwargs)
        form2 = UserCreationForm() # create an instance of the user form

        # add user form to context to be displayed in the html
        context['form2'] = form2

        return context
    
    def form_valid(self, form):
        """handle for submission to include the user"""

        # create an instance of usercreationform with our inputs
        user_form = UserCreationForm(self.request.POST)
        user = user_form.save() # create the user from the form

        # log in as the user
        login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')

        # fill in the username field of the profile with user info
        form.instance.username = self.request.POST['username']
        form.instance.user = user

        # delegate to superclass
        return super().form_valid(form)
    

class CreateFollowView(LoginRequiredMixin, CreateView):
    """the view to ask a user if they want to follow a profile"""

    form_class = CreateFollowForm
    template_name = "mini_insta/create_follow_form.html"

    def dispatch(self, request, *args, **kwargs):
        """override to check if the user has permission to do this action"""
        pk = self.kwargs['pk']                # get the profile pk
        profile = Profile.objects.get(pk=pk)  # get the profile

        # check if there is currently a user
        if request.user.is_authenticated:
            # the user is not allowed to follow themselves
            if request.user == profile.user:
                return render(request, "mini_insta/permission_denied.html")
            
            user_profile = Profile.objects.get(user=request.user)

            # prevent the user from following the same profile again
            if Follow.objects.filter(follower_profile=user_profile,
                                     profile=profile):
                return render(request, "mini_insta/permission_denied.html")

        # else send the page normally
        return super().dispatch(request, *args, **kwargs)

    def get_login_url(self):
        """return url for login if not logged in"""
        return reverse('login')

    def get_context_data(self, **kwargs):
        """add the profile the user is trying to follow into context"""
        context = super().get_context_data(**kwargs)
        pk = self.kwargs['pk']
        profile = Profile.objects.get(pk=pk)

        context['profile'] = profile

        return context
    
    def form_valid(self, form):
        """create the follow by finding user and profile"""
        user = self.request.user    # find user and the profile of user
        follower_profile = Profile.objects.get(user=user)
        pk = self.kwargs['pk']      # find followee profile
        profile = Profile.objects.get(pk=pk)

        # add them to form to make the follow
        form.instance.follower_profile = follower_profile
        form.instance.profile = profile

        return super().form_valid(form)

    def get_success_url(self):
        """after following, send back to their profile page"""
        return reverse('show_profile', kwargs={'pk':self.kwargs['pk']})


class DeleteFollowView(LoginRequiredMixin, DeleteView):
    """the view to ask a user if they want to stop following a profile"""

    template_name = "mini_insta/delete_follow_form.html"
    model = Follow

    def get_login_url(self):
        """return url for login if not logged in"""
        return reverse('login')

    def get_object(self, queryset = None):
        """find the object to be deleted"""
        user = self.request.user    # find the user
        user_profile = Profile.objects.get(user=user)
        pk = self.kwargs['pk']      # find the profile
        profile = Profile.objects.get(pk=pk)
        
        # use the user and profile to find the follow
        return Follow.objects.get(follower_profile=user_profile, profile=profile)

    def get_context_data(self, **kwargs):
        """add the profile the user is trying to remove into context"""
        context = super().get_context_data(**kwargs)
        pk = self.kwargs['pk']
        profile = Profile.objects.get(pk=pk)

        context['profile'] = profile

        return context
    
    def get_success_url(self):
        """redirect to profile after unfollowing"""
        return reverse('show_profile', kwargs={'pk':self.kwargs['pk']})
    

class CreateLikeView(LoginRequiredMixin, CreateView):
    """the view to ask the user if they want to like a post"""

    form_class = CreateLikeForm
    template_name = "mini_insta/create_like_form.html"

    def dispatch(self, request, *args, **kwargs):
        """override to check if the user has permission to do this action"""
        pk = self.kwargs['pk']                # get the post pk
        post = Post.objects.get(pk=pk)  # get the post

        # check if there is currently a user
        if request.user.is_authenticated:
            # the user is not allowed to like their own post
            if request.user == post.profile.user:
                return render(request, "mini_insta/permission_denied.html")
            
            user_profile = Profile.objects.get(user=request.user)

            # prevent the user from liking the same post again
            if Like.objects.filter(post=post,
                                   profile=user_profile):
                return render(request, "mini_insta/permission_denied.html")

        # else send the page normally
        return super().dispatch(request, *args, **kwargs)

    def get_login_url(self):
        """return url for login if not logged in"""
        return reverse('login')
    
    def get_context_data(self, **kwargs):
        """add the post the user is trying to like into context"""
        context = super().get_context_data(**kwargs)
        pk = self.kwargs['pk']
        post = Post.objects.get(pk=pk)

        context['post'] = post

        return context
    
    def form_valid(self, form):
        """create the like by finding post and profile"""
        user = self.request.user    # find user and the profile of user
        user_profile = Profile.objects.get(user=user)
        pk = self.kwargs['pk']      # find the post with pk
        post = Post.objects.get(pk=pk)

        # add them to form to make the like
        form.instance.post = post
        form.instance.profile = user_profile

        return super().form_valid(form)
    
    def get_success_url(self):
        """after liking, send back to post page"""
        return reverse('show_post', kwargs={'pk':self.kwargs['pk']})
    

class DeleteLikeView(LoginRequiredMixin, DeleteView):
    """view to delete a like"""

    template_name = "mini_insta/delete_like_form.html"
    model = Like

    def get_login_url(self):
        """return url for login if not logged in"""
        return reverse('login')
    
    def get_object(self, queryset = None):
        """find the object to be deleted"""
        user = self.request.user    # find the user
        user_profile = Profile.objects.get(user=user)
        pk = self.kwargs['pk']      # find the profile
        post = Post.objects.get(pk=pk)
        
        # use the user and post to find the like
        return Like.objects.get(post=post, profile=user_profile)
    
    def get_context_data(self, **kwargs):
        """add the post the user is trying to remove like into context"""
        context = super().get_context_data(**kwargs)
        pk = self.kwargs['pk']
        post = Post.objects.get(pk=pk)

        context['post'] = post

        return context
    
    def get_success_url(self):
        """redirect to post after unliking"""
        return reverse('show_post', kwargs={'pk':self.kwargs['pk']})