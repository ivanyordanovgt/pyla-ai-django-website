from django.contrib import admin

# Register your models here.
from pyla.subscriptions.models import Subscription, Features


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    pass


@admin.register(Features)
class SubscriptionFeatures(admin.ModelAdmin):
    pass
