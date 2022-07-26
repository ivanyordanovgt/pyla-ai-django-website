from django.urls import path

from pyla.forums.views import ForumsListView, ForumsPostsListView, PostsCommentsListView, EditPostView, DeletePostView
from pyla.forums.views import CreateCommentView, CreatePostView
urlpatterns = [

    path('forums/', ForumsListView.as_view(), name='show forums page'),
    path('forum/<int:pk>/', ForumsPostsListView.as_view(), name="show forums posts"),
    path('post/comments/<int:pk>/', PostsCommentsListView.as_view(), name='show posts comments'),
    path('create-comment/<int:pk>/', CreateCommentView.as_view(), name='create comment'),
    path('create-post/<int:pk>/', CreatePostView.as_view(), name='create post'),
    path('edit-post/<int:pk>/', EditPostView.as_view(), name='edit post'),
    path('delete-post/<int:pk>/', DeletePostView.as_view(), name='delete post'),
]