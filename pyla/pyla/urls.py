from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('pyla.web.urls')),
    path('subscriptions/', include('pyla.subscriptions.urls')),
    # path('test/', include('pyla.web_testing.urls')),
    path('user/', include('pyla.manage_profiles.urls')),
    path('forum/', include('pyla.forums.urls')),
    path('activity/', include('pyla.user_activity.urls')),
    path('administrate/', include('pyla.administrate.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('betscrapper/', include('pyla.betscrapper.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
