from django.urls import path

from pyla.betscrapper.views import *
urlpatterns = [
    path("", BetsView.as_view(), name='bets list'),
    path("refresh", RefreshDataView.as_view(), name='refresh data'),
    path('match/<int:pk>/', MatchDetailView.as_view(), name='show match details'),
]