from django.urls import path

from pyla.user_activity.views import ContactUsView, FeedbackActivityView, FeedbackMessageView, ActivityView, cache_test
from pyla.user_activity.views import FeedbackReplyView, FeedbackRepliesListView, PostsListView
urlpatterns = [
    path('', ActivityView.as_view(), name='activity'),


    path('feedback-submit/', ContactUsView.as_view(), name='feedback'),
    path('feedback-view/<int:pk>/', FeedbackMessageView.as_view(), name='view feedback message'),
    path('feedback/reply/<int:pk>/', FeedbackReplyView.as_view(), name='reply to feedback'),
    path('feedback/replies/view/<int:pk>/', FeedbackRepliesListView.as_view(), name='view feedback replies'),
    path('messages/<int:pk>/', FeedbackActivityView.as_view(), name='view feedback activity'),
    path('posts/', PostsListView.as_view(), name='show personal posts'),


    path('cache-test', cache_test, name='cache test'),
]

import pyla.user_activity.signals
