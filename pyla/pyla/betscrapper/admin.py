from django.contrib import admin

# Register your models here.
from pyla.betscrapper.models import BetMatch


@admin.register(BetMatch)
class BetMatch(admin.ModelAdmin):
    pass