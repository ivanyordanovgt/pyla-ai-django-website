from django import test as django_test
from django.contrib.auth import get_user_model, login
from django.urls import reverse

from pyla.administrate.models import StaffGroup
from pyla.manage_profiles.models import Profile
from pyla.web.models import IndexConfigurator, AboutPylaTextConfigurator

UserModel = get_user_model()


class AdministrateTests(django_test.TestCase):
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

    # administrate view test
    def test_access_administrate_with_no_rights__expect_404(self):
        user, profile = self.__create_valid_user_profile()
        self.client.login(**self.VALID_USER_CREDENTIALS)
        response = self.client.get()

        self.assertTemplateUsed(response=response, template_name='exception_handling/403.html')

    def test_access_administrate_with_rights_expect_200(self):
        staff_group = self.__create_valid_staff_group(
            title='test',
        )
        index_config = IndexConfigurator.objects.create(pyla_moto='SOFTUNI TEST')

        user, profile = self.__create_valid_user_profile(staff_group=staff_group)
        self.client.login(**self.VALID_USER_CREDENTIALS)
        response = self.client.get()

        self.assertEqual(200, response.status_code)

    def test_access_feedback_no_user__expect_redirect_to_login(self):
        self.client.get()
        self.assertTemplateUsed('manage_profiles/auth/login.html')

    def test_access_feedback__expect_200(self):
        user, profile = self.__create_valid_user_profile()
        self.client.login(**self.VALID_USER_CREDENTIALS)
        response = self.client.get()
        self.assertEqual(200, response.status_code)

    def test_access_handle_feedback_with_no_rights_anonymous__expect_403(self):
        response = self.client.get()
        self.assertTemplateUsed(response=response, template_name='exception_handling/403.html')

    def test_access_handle_feedback_with_no_rights_logged_in_expect_403(self):
        self.__create_valid_user_profile()
        self.client.login(**self.VALID_USER_CREDENTIALS)

        response = self.client.get()
        self.assertTemplateUsed(response=response, template_name='exception_handling/403.html')

    def test_access_handle_feedback_with_rights__expect_200(self):
        staff_group = self.__create_valid_staff_group(
            title='test',
            response_to_feedback=True,
        )
        index_config = IndexConfigurator.objects.create(pyla_moto='SOFTUNI TEST')

        user, profile = self.__create_valid_user_profile(staff_group=staff_group)
        self.client.login(**self.VALID_USER_CREDENTIALS)
        response = self.client.get()

        self.assertEqual(200, response.status_code)

    def test_configure_about_page_mixin_anonymous__expect_403(self):

        AboutPylaTextConfigurator.objects.create(goals_text='1', about_pyla_text='2')
        response = self.client.get()
        self.assertTemplateUsed(response=response, template_name='exception_handling/403.html')

    def test_configure_about_page_mixin_no_rights__expects_403(self):
        self.__create_valid_user_profile()
        self.client.login(**self.VALID_USER_CREDENTIALS)
        AboutPylaTextConfigurator.objects.create(goals_text='1', about_pyla_text='2')
        response = self.client.get()
        self.assertTemplateUsed(response=response, template_name='exception_handling/403.html')

    def test_create_subscription_mixin__expect_403(self):

        response = self.client.get()
        self.assertTemplateUsed(response=response, template_name='exception_handling/403.html')

    def test_create_subscription_mixin_logged_in__expect_403(self):
        self.__create_valid_user_profile()
        self.client.login(**self.VALID_USER_CREDENTIALS)
        response = self.client.get()
        self.assertTemplateUsed(response=response, template_name='exception_handling/403.html')

    def test_create_subscription_mixin_staff_rights__expect_correct_template(self):
        staff_group = self.__create_valid_staff_group(
            create_subscription=True,
        )

        self.__create_valid_user_profile(staff_group=staff_group)
        self.client.login(**self.VALID_USER_CREDENTIALS)
        response = self.client.get()
        self.assertTemplateUsed('subscriptions/create-subscription.html')
