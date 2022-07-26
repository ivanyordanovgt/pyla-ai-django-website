from django.apps import AppConfig

from pyla import web


class WebConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'pyla.web'
