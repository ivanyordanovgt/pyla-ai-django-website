import logging

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
import django.views.generic as views
from pyla.manage_profiles.mixins import CRUDAccessMixin
# Create your views here.
from django.urls import reverse_lazy

from pyla.subscriptions.forms import SubscriptionEditForm
from pyla.web.models import IndexConfigurator, AboutPylaPageConfigurator, AboutPylaTextConfigurator
from pyla.subscriptions.models import Subscription, Features


class SubscriptionsView(LoginRequiredMixin, views.ListView):
    model = Subscription

    def get_template_names(self):
        template_name = 'web/subscriptions.html'
        return template_name

    def __extract_valid_fields(self, obj_list=Subscription.objects.all()):
        subscriptions_features = {}
        for subscription in obj_list:
            features_list = []
            features_boolean = [x for x in
                                Features.objects.values_list().get()]
            logging.info(f"TITLE: {subscription.title}")
            feature_fields = [str(x).split('.')[-1] for x in Features._meta.fields]
            for i in range(len(features_boolean)):
                if features_boolean[i] is True:
                    features_list.append(feature_fields[i])
            subscriptions_features[f'{subscription.title}'] = features_list
        return subscriptions_features

    def __sort_subscription_by_len_of_features(self, subscriptions):
        subscriptions_features_new = {}
        while subscriptions:
            lowest_key = list(subscriptions.keys())[0]
            for key, value in subscriptions.items():
                if len(value) < len(subscriptions[lowest_key]):
                    lowest_key = key
            new_value = subscriptions[lowest_key]
            subscriptions.pop(lowest_key)
            subscriptions_features_new[lowest_key] = new_value
        return subscriptions_features_new

    def filter_subscriptions(self):
        subscriptions = self.__extract_valid_fields()
        subscriptions_sorted = self.__sort_subscription_by_len_of_features(subscriptions)

        obj_list = []
        for title, features in subscriptions_sorted.items():
            object = Subscription.objects.get(title=title)
            obj_list.append(object)
        return subscriptions_sorted, obj_list

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['features'] = Features._meta.fields
        subscriptions_features = {}
        features_list = []

        for subscription in Subscription.objects.all():
            features_boolean = [x for x in Features.objects.values_list().get()]
            feature_fields = [str(x).split('.')[-1] for x in Features._meta.fields]

            for i in range(len(features_boolean)):
                if features_boolean[i] is True:
                    features_list.append(feature_fields[i])
            subscriptions_features[f'{subscription.title}'] = features_list
            features_list = []

        subscriptions_features_new = {}

        while subscriptions_features:
            lowest_key = list(subscriptions_features.keys())[0]
            for key, value in subscriptions_features.items():
                if len(value) < len(subscriptions_features[lowest_key]):
                    lowest_key = key
            new_value = subscriptions_features[lowest_key]
            subscriptions_features.pop(lowest_key)
            subscriptions_features_new[lowest_key] = new_value

        obj_list = []

        for title, features in subscriptions_features_new.items():
            object = Subscription.objects.get(title=title)
            obj_list.append(object)

        context['features'] = subscriptions_features_new
        context['obj_list'] = obj_list
        return context

class SubscriptionsDetailsView(LoginRequiredMixin, views.DetailView):
    template_name = "subscriptions/subscription-details.html"
    model = Subscription

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class SubscriptionEditView(LoginRequiredMixin, CRUDAccessMixin, views.UpdateView):
    template_name = 'subscriptions/subscription-edit.html'
    model = Subscription
    form_class = SubscriptionEditForm

    def get_success_url(self):
        return reverse_lazy('show subscriptions')
