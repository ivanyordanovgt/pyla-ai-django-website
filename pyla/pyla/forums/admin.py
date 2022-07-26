from django.contrib import admin

# Register your models here.
from pyla.forums.models import Comment, Post, Forum


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    pass


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    pass


@admin.register(Forum)
class ForumAdmin(admin.ModelAdmin):
    pass
