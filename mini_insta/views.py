# mini_insta/views.py
# Aidan Xu (axu26@bu.edu), 9/24/25
# The views code used for the mini_insta app

from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.views.generic import *
from .models import *
from .forms import *

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
    context_object_name = "profile" # single profile


class PostDetailView(DetailView):
    """A view class to show more details of a single post"""

    model = Post
    template_name = "mini_insta/show_post.html"
    context_object_name = "post" # single post


class CreatePostView(CreateView):
    """A view to allow creation of a post with a form"""

    form_class = CreatePostForm
    template_name = "mini_insta/create_post_form.html"

    def get_context_data(self):
        """specifies context variables for the post create view"""

        # find the key of the profile, get the profile, then add it to the form
        context = super().get_context_data()
        pk = self.kwargs['pk']
        profile = Profile.objects.get(pk=pk)

        # add that profile to the context
        context['profile'] = profile

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

        # find the key of the profile, get the profile, then add it to the form
        pk = self.kwargs['pk']
        profile = Profile.objects.get(pk=pk)
        form.instance.profile = profile

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


class UpdateProfileView(UpdateView):
    """A view to update a profile with a form"""

    form_class = UpdateProfileForm
    template_name = "mini_insta/update_profile_form.html"
    model = Profile


class DeletePostView(DeleteView):
    """A view to prompt the user to delete a post"""

    template_name = "mini_insta/delete_post_form.html"
    model = Post

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


class UpdatePostView(UpdateView):
    """A view to update a post"""

    form_class = UpdatePostForm
    template_name = "mini_insta/update_post_form.html"
    model = Post

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
    

class DeletePhotoView(DeleteView):
    """View to confirm delettion of a photo"""

    template_name = "mini_insta/delete_photo_form.html"
    model = Photo

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


class ShowFollowingDetailView(DetailView):
    """view showing all a profile's follows"""

    model = Profile
    template_name = "mini_insta/show_following.html"
    context_object_name = "profile"


class PostFeedListView(ListView):
    """view showing all posts for a user's feed"""

    model = Post
    template_name = "mini_insta/show_feed.html"
    context_object_name = "posts" # all posts

    def get_context_data(self):
        """specifies context variables for feed"""

        # find the key of the profile and get it
        context = super().get_context_data()
        pk = self.kwargs['pk']
        profile = Profile.objects.get(pk=pk)

        # add that profile to the context
        context['profile'] = profile

        return context
    

class SearchView(ListView):
    """view that gives the user a search bar to find posts/profiles"""

    template_name = "mini_insta/search_results.html"

    def dispatch(self, request, *args, **kwargs):
        """override the superclass dispatch method"""

        # if there is no query made yet, send the search form
        if not 'query' in self.request.GET:
            # find profile of the user making search and put it into context
            pk = self.kwargs['pk']
            profile = Profile.objects.get(pk=pk)
            context = {
                "profile": profile,
            }
            return render(request, "mini_insta/search.html", context)

        # else show the results of query
        return super().dispatch(request, *args, **kwargs)
    
    def get_queryset(self):
        """returns a queryset of posts based on the query"""
        query = self.request.GET['query']

        # get the query set of posts from the caption
        qs_caption = Post.objects.filter(caption__contains=query)

        return qs_caption

    def get_context_data(self, **kwargs):
        """specifies context variables for search"""

        # find the key of the profile and get it
        context = super().get_context_data(**kwargs)
        pk = self.kwargs['pk']
        profile = Profile.objects.get(pk=pk)

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