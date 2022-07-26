from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
import django.views.generic as views

# Create your views here.
from django.urls import reverse_lazy

from pyla.administrate.mixins import StaffMixin, ConfigureIndexMixin, ConfigureAboutPageMixin, CreateSubscriptionMixin, \
    HandleFeedbackMixin
from pyla.manage_profiles.models import Profile, ContactUs
from pyla.subscriptions.models import Subscription, Features
from pyla.web.models import IndexConfigurator, AboutPylaTextConfigurator

UserModel = get_user_model()


class AdministrateView(StaffMixin, LoginRequiredMixin, views.TemplateView):
    template_name = 'administrate/administrate-page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user.profile.staff_group
        config = IndexConfigurator.objects.all()[0]
        return context


class HandleFeedback(HandleFeedbackMixin, views.ListView):
    model = ContactUs
    template_name = 'administrate/feedback/handle-feedback.html'
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        filtered_feedback = ContactUs.objects.filter(status=False)
        return super(HandleFeedback, self).get_context_data(object_list=filtered_feedback)

class ConfigureIndexView(ConfigureIndexMixin, views.UpdateView):
    model = IndexConfigurator
    template_name = 'administrate/configure-index.html'
    fields = ('pyla_moto',)

    def get_success_url(self):
        return reverse_lazy('administrate page')


class ConfigureAboutPageView(ConfigureAboutPageMixin, views.UpdateView):
    model = AboutPylaTextConfigurator
    template_name = 'administrate/configure-about-page.html'
    fields = ('about_pyla_text', 'goals_text',)

    def get_success_url(self):
        return reverse_lazy('administrate page')


class SubscriptionConfigurator(CreateSubscriptionMixin, views.TemplateView):
    template_name = 'administrate/subscription-configurator.html'


class CreateSubscriptionView(CreateSubscriptionMixin, views.CreateView):
    model = Subscription
    fields = '__all__'
    template_name = 'subscriptions/create-subscription.html'

    def get_success_url(self):
        return reverse_lazy("configure subscriptions")


class CreateFeatureView(LoginRequiredMixin, CreateSubscriptionMixin, views.CreateView):
    model = Features
    fields = '__all__'
    template_name = 'subscriptions/create-features.html'

    def get_success_url(self):
        return reverse_lazy("configure subscriptions")


class FeaturesListView(CreateSubscriptionMixin, views.ListView):
    model = Features
    template_name = 'subscriptions/features-list.html'


class EditFeatureView(CreateSubscriptionMixin, views.UpdateView):
    model = Features
    template_name = 'subscriptions/edit-feature.html'
    fields = '__all__'

    def get_success_url(self):
        return reverse_lazy('configure features')


class DeleteFeatureView(CreateSubscriptionMixin, views.DeleteView):
    model = Features
    template_name = 'subscriptions/features-delete.html'

    def get_success_url(self):
        return reverse_lazy('configure features')


class SubscriptionListView(CreateSubscriptionMixin, views.ListView):
    model = Subscription
    template_name = 'subscriptions/subscriptions-list.html'


class SubscriptionDeleteView(CreateSubscriptionMixin, views.DeleteView):
    model = Subscription
    template_name = 'subscriptions/subscription-delete.html'

    def get_success_url(self):
        return reverse_lazy('configure - subscription list')


class FeedbackStatusChangeView(HandleFeedbackMixin, views.UpdateView):
    model = ContactUs
    fields = ('status',)
    template_name = 'administrate/feedback/change-status-feedback.html'

    def get_context_data(self, **kwargs):
        context = super(FeedbackStatusChangeView, self).get_context_data()
        context['feedback_pk'] = self.kwargs['pk']
        return context

    def get_success_url(self):
        return reverse_lazy('handle feedback page')
