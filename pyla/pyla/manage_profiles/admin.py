from django.contrib import admin

# Register your models here.
from pyla.manage_profiles.models import Profile, AppUser, ContactUs, EmailKey
from pyla.user_activity.models import FeedbackReply


@admin.register(AppUser)
class AppUserAdmin(admin.ModelAdmin):
    pass


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    pass


@admin.register(ContactUs)
class ContactUsAdmin(admin.ModelAdmin):
    pass


@admin.register(EmailKey)
class EmailKeyAdmin(admin.ModelAdmin):
    pass
