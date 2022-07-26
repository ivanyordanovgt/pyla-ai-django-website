import logging
import random
from itertools import chain

import django.views.generic as views
from django.contrib.auth import forms as auth_forms, get_user_model, login
from django.contrib.auth import views as auth_views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import ModelForm
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy, reverse
from django import forms
from django.views.decorators.cache import cache_page

from pyla.forums.models import Post
from pyla.manage_profiles.forms import ProfileForm, CreateFeedbackForm, ReplyToFeedbackForm
from pyla.manage_profiles.mixins import CRUDAccessMixin
from pyla.manage_profiles.models import Profile, ContactUs, AppUser
from pyla.user_activity.mixins import HandleReplyMixin
from pyla.user_activity.models import FeedbackReply

UserModel = get_user_model()


class ContactUsView(LoginRequiredMixin, views.CreateView):
    MAX_MESSAGES_PER_USER = 3

    model = ContactUs
    template_name = 'web/contact_us.html'
    form_class = CreateFeedbackForm

    def get_success_url(self):
        return reverse_lazy('index')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get(self, request, *args, **kwargs):
        feedback_messages = ContactUs.objects.filter(user_id=self.request.user.pk)
        feedback_messages = feedback_messages.filter(status=False)

        if len(feedback_messages) >= self.MAX_MESSAGES_PER_USER:
            return render(request, 'exception_handling/no-feedback-submit-access.html')
        #
        # if len(feedback_no_answer) > self.MAX_MESSAGES_PER_USER:
        #     return render()
        return super().get(request, *args, **kwargs)


class ActivityView(views.TemplateView):
    template_name = 'user_activity/activity-page.html'


class FeedbackMessageView(views.DetailView):
    model = ContactUs
    template_name = 'user_activity/feedback-view.html'
    MAX_UNANSWERED_FEEDBACKS = 4

    def get_context_data(self, **kwargs):
        context = super(FeedbackMessageView, self).get_context_data()
        feedback_replies = FeedbackReply.objects.filter(feedback=context['object'])
        context['replies'] = feedback_replies
        context['replies_count'] = len(feedback_replies)
        return context


class FeedbackListView(views.ListView):
    pass


class FeedbackReplyView(HandleReplyMixin, views.CreateView):
    model = FeedbackReply
    form_class = ReplyToFeedbackForm
    template_name = 'user_activity/reply-to-feedback.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        feedback_obj = ContactUs.objects.get(pk=self.kwargs['pk'])
        kwargs['feedback'] = feedback_obj
        kwargs['user'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form_kwargs = self.get_form_kwargs()
        context['feedback_pk'] = form_kwargs['feedback']
        return context

    def get_success_url(self):
        return (reverse('view feedback message',
                        kwargs={
                            'pk': self.kwargs['pk'],
                        }))


class FeedbackRepliesListView(views.ListView):
    model = FeedbackReply
    template_name = 'user_activity/feedback-replies-view.html'

    def __return_replies(self):
        return FeedbackReply.objects.filter(feedback_id=self.kwargs['pk']).order_by('-date')

    def get_context_data(self, *, object_list=None, **kwargs):
        object_list = self.__return_replies()
        context = super(FeedbackRepliesListView, self).get_context_data(object_list=object_list)
        context['feedback_pk'] = self.kwargs['pk']
        return context


class FeedbackActivityView(LoginRequiredMixin, CRUDAccessMixin, views.ListView):
    MAX_UNANSWERED_FEEDBACKS = 4
    template_name = 'user_activity/activity.html'
    model = ContactUs

    def get_queryset(self):
        feedbacks = ContactUs.objects.filter(user_id=self.kwargs['pk'])
        unanswared_feedbacks = feedbacks.filter(status=False)
        answered_feedbacks = feedbacks.filter(status=True)

        return list(chain(unanswared_feedbacks, answered_feedbacks))

    def get(self, request, *args, **kwargs):
        return super(FeedbackActivityView, self).get(request, *args, **kwargs)


class PostsListView(LoginRequiredMixin, views.ListView):
    template_name = 'user_activity/posts-list.html'

    def get_queryset(self):
        return Post.objects.filter(user_id=self.request.user.pk)


@cache_page(30)
def cache_test(request):
    return HttpResponse(f"CACHED NUMBER ->{random.randint(1, 1024)}")
