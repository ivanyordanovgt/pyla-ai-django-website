from django import test as django_test
from django.contrib.auth import get_user_model, login
from django.urls import reverse

from pyla.administrate.models import StaffGroup
from pyla.manage_profiles.models import Profile
from pyla.subscriptions.models import Subscription, Features
from pyla.web.models import IndexConfigurator, AboutPylaTextConfigurator
from pyla.subscriptions.views import SubscriptionsView

UserModel = get_user_model()

"""

TEST THE FOLLOWING FUNCTIONS.

"""


def extract_valid_fields(obj_list=Subscription.objects.all()):
    subscriptions_features = {}
    for subscription in obj_list:
        features_list = []
        features_boolean = [x for x in
                            Features.objects.values_list().get()]
        feature_fields = [str(x).split('.')[-1] for x in Features._meta.fields]
        for i in range(len(features_boolean)):
            if features_boolean[i] is True:
                features_list.append(feature_fields[i])
        subscriptions_features[f'{subscription.title}'] = features_list
    return subscriptions_features



class TestSort(django_test.TestCase):

    DESCRIPTION = 'RANDOM TEXT'
    TITLE = 'TEST-ONE'

    def test__expect_correct_list(self):
        features_object = Features.objects.create(
            name=f'{self.TITLE}',
            ESP=True,
            lines=True,
        )
        subscription = Subscription.objects.create(
            title=f'{self.TITLE}',
            description=self.DESCRIPTION,
            features=features_object,
        )

        subscription_features = extract_valid_fields()

        EXPECTED_RESULT = {f'{self.TITLE}': ['ESP', 'lines']}
        self.assertEqual(EXPECTED_RESULT, subscription_features)

    def test_with_false_fields__expect_correct_list(self):
        features_object = Features.objects.create(
            name=f'{self.TITLE}',
            ESP=True,
            lines=True,
            autoplay=False,
            advanced_in_depth_gameplay=False,
        )
        subscription = Subscription.objects.create(
            title=f'{self.TITLE}',
            description=self.DESCRIPTION,
            features=features_object,
        )

        subscription_features = extract_valid_fields()

        EXPECTED_RESULT = {f'{self.TITLE}': ['ESP', 'lines']}
        self.assertEqual(EXPECTED_RESULT, subscription_features)

    def test_with_no_fields__expect_correct_list(self):
        features_object = Features.objects.create(
            name=f'{self.TITLE}',
        )
        subscription = Subscription.objects.create(
            title=f'{self.TITLE}',
            description=self.DESCRIPTION,
            features=features_object,
        )

        subscription_features = extract_valid_fields()

        EXPECTED_RESULT = {f'{self.TITLE}': []}
        self.assertEqual(EXPECTED_RESULT, subscription_features)
