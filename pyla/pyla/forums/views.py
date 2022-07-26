from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
# Create your views here.
from django.views import generic as views
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from pyla.forums import models as forums
from pyla.forums.forms import PostCommentForm, PostForm
from pyla.forums.mixins import PostCRUDMixin
from pyla.manage_profiles.models import Profile


class ForumsListView(LoginRequiredMixin, views.ListView):
    template_name = 'forums/forums.html'
    model = forums.Forum

    def get_context_data(self, *, object_list=None, **kwargs):
        forums_list = forums.Forum.objects.all()
        context = super(ForumsListView, self).get_context_data(object_list=forums_list)
        context['forums_list'] = forums_list
        return context


class ForumsPostsListView(LoginRequiredMixin, views.ListView):
    model = forums.Post
    template_name = 'forums/posts-inside-forum.html'
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        posts_list = forums.Post.objects.filter(forum_id=self.kwargs['pk']).order_by('-date')
        forum = forums.Forum.objects.get(pk=self.kwargs['pk'])
        postCounter = {}

        for post in posts_list:
            postCounter[f'{post}'] = post.comment_set.count()

        context = super(ForumsPostsListView, self).get_context_data(object_list=posts_list)
        context['forums_list'] = forums.Forum.objects.all()
        context['current_forum_title'] = forum.title
        context['forum_pk'] = self.kwargs['pk']

        data = {'ok': 1, 'okay': 2}
        context['data'] = data
        context['comments'] = postCounter
        context['forumDesc'] = forum.description
        context['postsCount'] = forum.post_set.count()
        context['forumObj'] = forum

        return context


class PostsCommentsListView(LoginRequiredMixin, views.CreateView):
    model = forums.Comment
    template_name = 'forums/comments-inside-post.html'
    form_class = PostCommentForm
    
    def post(self, request, *args, **kwargs):

        if not self.request.user.is_activated:

            return redirect('email confirmation')
        return super(PostsCommentsListView, self).post(request, *args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PostsCommentsListView, self).get_context_data()

        post = forums.Post.objects.get(pk=self.kwargs['pk'])
        comments = post.comment_set.all()
        context['object_list'] = comments.order_by('-date')
        context['post'] = post

        return context

    def get_form_kwargs(self):
        kwargs = super(PostsCommentsListView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        kwargs['post'] = forums.Post.objects.get(pk=self.kwargs['pk'])
        return kwargs

    def get_success_url(self):
        return reverse(
            'show posts comments',
            kwargs={
                'pk': self.kwargs['pk']
            }
        )


class CreateCommentView(LoginRequiredMixin, views.CreateView):
    model = forums.Comment
    template_name = 'forums/create_comment.html'
    form_class = PostCommentForm
    
    def post(self, request, *args, **kwargs):

        if not self.request.user.is_activated:

            return redirect('email confirmation')
        return super(CreateCommentView, self).post(request, *args, **kwargs)
    

    def get_form_kwargs(self):
        kwargs = super(CreateCommentView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        kwargs['post'] = forums.Post.objects.get(pk=self.kwargs['pk'])
        return kwargs

    def get_success_url(self):
        return reverse(
            'show posts comments',
            kwargs={
                'pk': self.kwargs['pk']
            }
        )


class CreatePostView(views.CreateView):
    POST_COST = 100

    model = forums.Post
    form_class = PostForm
    def get_template_names(self):

        if self.request.user.profile.balance < self.POST_COST:
            return 'forums/notEnoughBalance.html'
        else:
            return 'forums/create-post.html'

    def get(self, request, *args, **kwargs):

        if not self.request.user.is_activated:

            return redirect('email confirmation')
        return super(CreatePostView, self).get(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(CreatePostView, self).get_form_kwargs()
        kwargs['forum'] = forums.Forum.objects.get(pk=self.kwargs['pk'])
        kwargs['user'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(CreatePostView, self).get_context_data()
        context['forums_list'] = forums.Forum.objects.all()
        context['forum_id'] = self.kwargs['pk']
        return context

    def get_success_url(self):
        user = Profile.objects.get(pk=self.request.user.profile.pk)
        user.balance -= 100
        user.save()
        return reverse(
            'show forums posts',
            kwargs={
                'pk': self.kwargs['pk']
            }

        )


class EditPostView(PostCRUDMixin, views.UpdateView):
    model = forums.Post
    fields = ('title', 'description')
    template_name = 'forums/edit-post.html'

    def get_context_data(self, **kwargs):
        context = super(EditPostView, self).get_context_data()
        context['forums_list'] = forums.Forum.objects.all()
        context['forum_id'] = context['object'].forum.pk
        return context

    def get_success_url(self):
        return reverse(
            'show posts comments',
            kwargs={
                'pk': self.kwargs['pk'],
            }
        )


class DeletePostView(PostCRUDMixin, views.DeleteView):

    model = forums.Post
    template_name = 'forums/delete-post.html'

    def get_context_data(self, **kwargs):
        context = super(DeletePostView, self).get_context_data()
        context['post_pk'] = self.kwargs['pk']
        return context
    def get_success_url(self):
        return reverse(
            'show forums page',

        )