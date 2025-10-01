from django.shortcuts import render, redirect
from django.db.models import Q
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.views import View
from .models import Post, Comment, UserProfile, WeeklyScore
from .forms import PostForm, CommentForm, ProfileEditForm
from users.models import CustomUser
from django.utils.timezone import now
from datetime import timedelta
import random

# Create your views here.
class PostList(LoginRequiredMixin,View):
    def get(self, request, *args, **kwargs):
        logged_in_user = request.user
        # logged_in_user = CustomUser.objects.get(pk=logged_in_user.pk) 
        followed_posts = Post.objects.filter(
            Q(author__profile__followers=logged_in_user) | Q(author=logged_in_user)
        ).distinct().order_by('-created_on')

        unfollowed_posts = Post.objects.exclude(
            Q(author__profile__followers=logged_in_user) | Q(author=logged_in_user)
        ).distinct()

        RANDOM_UNFOLLOWED_LIMIT = 5
        unfollowed_post_ids = list(unfollowed_posts.values_list('id', flat=True))
        random.shuffle(unfollowed_post_ids)
        random_sample_ids = unfollowed_post_ids[:RANDOM_UNFOLLOWED_LIMIT]
        random_posts = Post.objects.filter(id__in=random_sample_ids)


        combined_posts = Post.objects.filter(
            Q(id__in=list(followed_posts.values_list('id', flat=True))) |
            Q(id__in=list(random_posts.values_list('id', flat=True)))
)       .order_by('-created_on')



        #form = PostForm()
        def get_week_start():
            today = now().date()
            return today - timedelta(days=today.weekday())

        week_start = get_week_start()
        top_users = WeeklyScore.objects.filter(week_start=week_start).select_related('user').order_by('-score')[:10]

        # top_users = CustomUser.objects.order_by('-score')[:10]

        context = {
            'post_list' : combined_posts,
            #'form' : form,
            'top_users' : top_users,
        }

        return render(request, 'social/post_list.html', context)

# def PostCreate(request):
#   if request.method == 'POST':
#       form = PostForm(request.POST, request.FILES)
#       if form.is_valid():
#           form.save()
#           return redirect('postlist')
#   else:
#       form = PostForm()

#   return render(request, 'social/post_create.html', {'form' : form})

class PostCreate(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        form = PostForm()
            
        context = {
            'form' : form,
        }
            
        return render(request, 'social/post_create.html', context)

    def post(self, request, *args, **kwargs):
        form = PostForm(request.POST, request.FILES)
        
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.author = request.user
            new_post.save() 

        return redirect('postlist')

class PostDetail(LoginRequiredMixin,View):
    def get(self, request, pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)
        form = CommentForm()
        comments = Comment.objects.filter(post=post).order_by('-created_on')

        context = {
            'post' : post,
            'form' : form,
            'comments' : comments,

        }
        return render(request, 'social/post_detail.html', context)

    def post(self, request, pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)
        form = CommentForm(request.POST)

        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.author = request.user
            new_comment.post = post
            new_comment.save() 

        # comments = Comment.objects.filter(post=post).order_by('-created_on')

        # context = {
        #   'post' : post,
        #   'form' : form,
        #   'comments' : comments,
        # }

        return redirect('postdetail', post.pk)

class PostUpdate(LoginRequiredMixin, UserPassesTestMixin,UpdateView):
    model = Post
    fields = ['body']
    template_name = 'social/post_edit.html'

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy('postdetail', kwargs={'pk': pk})

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

class PostDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'social/post_delete.html'

    def get_success_url(self):
        pk = self.kwargs['profile_pk']
        return reverse_lazy('profileview', kwargs={'pk' : pk})

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

class CommentDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'social/comment_delete.html'

    def get_success_url(self):
        pk = self.kwargs['post_pk']
        return reverse_lazy('postdetail', kwargs={'pk': pk})

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

class Profile(View):
    def get(self, request, pk, *args, **kwargs):
        profile = UserProfile.objects.get(pk=pk)
        user = profile.user
        posts = Post.objects.filter(author=user).order_by('-created_on')

        followers = profile.followers.all()

        if len(followers) == 0:
            is_following = False

        for follower in followers:
            if follower == request.user:
                is_following = True
                break
            else:
                is_following = False

        number_of_followers = len(followers)

        context = {
            'user' : user,
            'profile' : profile,
            'posts' : posts,
            'number_of_followers' : number_of_followers,
            'is_following' : is_following,
        }

        return render(request, 'social/profiles.html', context)

class ProfileEdit(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = UserProfile
    form_class = ProfileEditForm
    template_name = 'social/profile_edit.html'

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy('profileview', kwargs={'pk' : pk})

    def test_func(self):
        profile = self.get_object()
        return self.request.user == profile.user

class AddFollower(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        profile = UserProfile.objects.get(pk=pk)
        profile.followers.add(request.user)

        return redirect('profileview', pk=profile.pk)

class RemoveFollower(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        profile = UserProfile.objects.get(pk=pk)
        profile.followers.remove(request.user)

        return redirect('profileview', pk=profile.pk)

class AddLike(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)

        is_dislike = False
        
        for dislike in post.dislikes.all():
            if dislike == request.user:
                is_dislike = True
                break

        if is_dislike:
            post.dislikes.remove(request.user)

        is_like = False
        
        for like in post.likes.all():
            if like == request.user:
                is_like = True
                break

        if not is_like:
            post.likes.add(request.user)

        if is_like:
            post.likes.remove(request.user)

        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)

class AddDislike(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)

        is_like = False
        
        for like in post.likes.all():
            if like == request.user:
                is_like = True
                break

        if is_like:
            post.likes.remove(request.user)

        is_dislike = False
        
        for dislike in post.likes.all():
            if dislike == request.user:
                is_dislike = True
                break

        if not is_dislike:
            post.dislikes.add(request.user)

        if is_dislike:
            post.dislikes.remove(request.user)

        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)

class Search(View):
    def get(self, request, *args, **kwargs):
        query = self.request.GET.get('query')
        profile_list = UserProfile.objects.filter(
            Q(user__username__icontains=query)
            )

        context = {
            'profile_list' : profile_list
        }

        return render(request, 'social/search.html', context)

def leaderboard_view(request):
    def get_week_start():
            today = now().date()
            return today - timedelta(days=today.weekday())

    week_start = get_week_start()
    top_users = WeeklyScore.objects.filter(week_start=week_start).select_related('user').order_by('-score')[:100]

    return render(request, 'social/leaderboard.html', {'top_users' : top_users})
