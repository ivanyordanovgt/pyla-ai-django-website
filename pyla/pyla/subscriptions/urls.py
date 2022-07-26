from django.urls import path

from pyla.subscriptions.views import SubscriptionsView, SubscriptionsDetailsView, SubscriptionEditView

urlpatterns = [
    path('list/', SubscriptionsView.as_view(), name='show subscriptions'),
    path('details/<int:pk>/', SubscriptionsDetailsView.as_view(), name='subscription detail'),
    path('edit/<int:pk>/', SubscriptionEditView.as_view(), name='subscription edit'),
]