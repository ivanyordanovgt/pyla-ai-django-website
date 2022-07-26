from django.contrib import admin

# Register your models here.
from pyla.administrate.models import StaffGroup


@admin.register(StaffGroup)
class StaffGroupAdmin(admin.ModelAdmin):
    pass