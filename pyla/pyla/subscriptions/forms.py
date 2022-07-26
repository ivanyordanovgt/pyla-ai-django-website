from django import forms

from pyla.subscriptions.models import Subscription


class SubscriptionEditForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(SubscriptionEditForm, self).__init__(*args, **kwargs)
        self.fields['description'].widget.attrs.update({'placeholder': 'Enter your description'})


    class Meta:
        model = Subscription
        fields = ('description',)


