from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
import django.views.generic as views
from pyla.manage_profiles.models import Profile

# Create your views here.
from django.urls import reverse_lazy

# from pyla.web.forms import FeedbackForm
from pyla.web.models import IndexConfigurator, AboutPylaPageConfigurator, AboutPylaTextConfigurator
from pyla.subscriptions.models import Subscription, Features


def index(request):
    context = {
        'moto': IndexConfigurator.objects.values_list('pyla_moto', flat=True)[0]
    }

    return render(request, 'web/index.html', context)


class AboutPyla(views.TemplateView):
    template_name = 'web/about_us.html'
    config = 0

    def get_context_data(self, **kwargs):
        config = self.config
        context = super().get_context_data(**kwargs)
        # context['pyla_description'] = AboutPylaPageConfigurator.objects.values_list('about_pyla_text', flat=True)[config]
        # context['pyla_goals'] = AboutPylaPageConfigurator.objects.values_list('goals_text', flat=True)[config]
        context['description'] = AboutPylaTextConfigurator.objects.values_list('about_pyla_text', flat=True)[config]
        context['goals'] = AboutPylaTextConfigurator.objects.values_list('goals_text', flat=True)[config]
        #

        return context


class RedirectToIndex(views.RedirectView):
    url = reverse_lazy('index')


# class ContactUsView(views.CreateView):
#
#     model = Feedback
#     template_name = 'web/contact_us.html'
#     form_class = FeedbackForm
#
#     def get_form_kwargs(self):
#         kwargs = super().get_form_kwargs()
#         kwargs['user'] = self.request.user
#         return kwargs

def forums_page(request):
    return render(request, 'web/../../templates/forums/forums.html')
