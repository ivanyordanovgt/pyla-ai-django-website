import random

from django import test as django_test
from django.contrib.auth import get_user_model
from django.urls import reverse

from pyla.administrate.models import StaffGroup
from pyla.manage_profiles.models import Profile, ContactUs

UserModel = get_user_model()


class Test(django_test.TestCase):
    VALID_USER_CREDENTIALS = {
        'email': 'djangotesting@gmail.com',
        'nickname': 'djangotesting',
        'password': 'QweomASMDosfk23',
    }

    VALID_PROFILE_DATA = {
        'description': '',
        'profile_picture': '',
        'moto': '',
    }

    VALID_USER_CREDENTIALS_SECOND = {
        'email': 'softunitest2@gmail.com',
        'nickname': 'softunitest2',
        'password': 'SoFtUnTeSt2',
    }

    def __create_valid_user_profile(self, staff_group=None, different=False):
        self.staff_group = staff_group

        if not different:
            user = UserModel.objects.create_user(
                **self.VALID_USER_CREDENTIALS,
            )
            profile = Profile.objects.create(
                **self.VALID_PROFILE_DATA,
                user=user,
                staff_group=self.staff_group,
            )
        else:
            user = UserModel.objects.create_user(
                email='softunitest2@gmail.com',
                nickname='softunitest2',
                password='SoFtUnTeSt2',
            )
            profile = Profile.objects.create(
                **self.VALID_PROFILE_DATA,
                user=user,
            )

        return user, profile

    @staticmethod
    def __create_valid_staff_group(**kwargs):
        staff_group = StaffGroup.objects.create(
            **kwargs
        )
        return staff_group

    def test_try_to_spam_feedback__expect_correct_template(self):
        user, profile = self.__create_valid_user_profile()
        self.client.login(**self.VALID_USER_CREDENTIALS)

        for i in range(10):
            ContactUs.objects.create(title='123123121231', description='1231231232', user_id=user.id)

        response = self.client.get()

        self.assertTemplateUsed(response=response, template_name='exception_handling/no-feedback-submit-access.html')

    def test_try_to_submit_feedback__expect_200(self):
        user, profile = self.__create_valid_user_profile()
        self.client.login(**self.VALID_USER_CREDENTIALS)
        response = self.client.get()

        self.assertTemplateUsed(response=response, template_name='web/contact_us.html')

    def test_try_to_reply_to_feedback_which_status_is_true__except_correct_template(self):
        user, profile = self.__create_valid_user_profile()
        self.client.login(**self.VALID_USER_CREDENTIALS)

        feedback = ContactUs.objects.create(title='111', description='1111', status=True, user_id=user.pk)

        response = self.client.get()

        self.assertTemplateUsed(response=response, template_name='exception_handling/403.html')
