from django.urls import path
from pyla.administrate.views import AdministrateView, ConfigureIndexView, ConfigureAboutPageView, \
    CreateSubscriptionView, FeedbackStatusChangeView
from pyla.administrate.views import SubscriptionConfigurator, CreateFeatureView, SubscriptionListView
from pyla.administrate.views import SubscriptionDeleteView, FeaturesListView, EditFeatureView, DeleteFeatureView
from pyla.administrate.views import HandleFeedback
urlpatterns = [
    path("", AdministrateView.as_view(), name='administrate page'),
    path('configurate-index/<int:pk>/', ConfigureIndexView.as_view(), name='configure index'),
    path('configurate-about-pyla-page/<int:pk>/', ConfigureAboutPageView.as_view(), name='configure about pyla'),
    path('create-subscription', CreateSubscriptionView.as_view(), name='create subscription'),
    path('create-feature', CreateFeatureView.as_view(), name='create feature'),
    path('features-list', FeaturesListView.as_view(), name='configure features'),
    path('feature-edit/<int:pk>/', EditFeatureView.as_view(), name='edit feature'),
    path('feature-delete/<int:pk>', DeleteFeatureView.as_view(), name='delete feature'),
    path('subscription-configurator/', SubscriptionConfigurator.as_view(), name='configure subscriptions'),
    path('subscriptions-list/', SubscriptionListView.as_view(), name='configure - subscription list'),
    path('subscriptions-delete/<int:pk>/', SubscriptionDeleteView.as_view(), name='delete subscription'),
    path('handle-feedback/', HandleFeedback.as_view(), name='handle feedback page'),
    path('close-feedback/<int:pk>/', FeedbackStatusChangeView.as_view(), name='close feedback'),
]
