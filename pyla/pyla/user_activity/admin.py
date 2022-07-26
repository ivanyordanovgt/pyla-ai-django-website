from django.contrib import admin

# Register your models here.
from pyla.user_activity.models import FeedbackReply


@admin.register(FeedbackReply)
class FeedbackReplyAdmin(admin.ModelAdmin):
    pass

