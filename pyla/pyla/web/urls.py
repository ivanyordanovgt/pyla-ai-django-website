from django.urls import path
from pyla.web.views import index, forums_page, \
    AboutPyla, RedirectToIndex

urlpatterns = [
    path('', RedirectToIndex.as_view(), name='redirect to index'),
    path('index/', index, name='index'),
    path('about-pyla/', AboutPyla.as_view(), name='about pyla'),
    # path('contact-us/', ContactUsView.as_view(), name='show contact us page'),
    path('ok/', index, name='show contact us page'),
]
