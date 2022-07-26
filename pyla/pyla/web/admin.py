from django.contrib import admin

# Register your models here.
from pyla.web.models import IndexConfigurator, AboutPylaPageConfigurator, AboutPylaTextConfigurator


@admin.register(IndexConfigurator)
class AdminIndexConfigurator(admin.ModelAdmin):
    pass


@admin.register(AboutPylaTextConfigurator)
class AdminAboutPylaPageConfigurator(admin.ModelAdmin):
    pass

