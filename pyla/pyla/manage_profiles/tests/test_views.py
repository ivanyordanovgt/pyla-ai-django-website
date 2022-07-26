import logging

from django import test as django_test
from django.contrib.auth import get_user_model, login
from django.urls import reverse

from pyla.administrate.models import StaffGroup
from pyla.manage_profiles.models import Profile

UserModel = get_user_model()


class ProfileTesting(django_test.TestCase):
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

    def test_view_non_existing_profile__anonymous__expect_302(self):
        """
            If user is not logged in he will be redirected to
            the login page.
            This will test if upon viewing an profile/non exi-
            sting profile, the web app will redirect to the
            login page
        """
        response = self.client.get()

        self.assertRedirects(response, '/user/login/?next=%2Fuser%2Fprofile%2F1', status_code=302,
                             target_status_code=200, fetch_redirect_response=True)

    def test_view_non_existing_profile__logged_in__expect_404(self):
        user, profile = self.__create_valid_user_profile()
        a = self.client.login(**self.VALID_USER_CREDENTIALS)
        logging.critical(f"---> {a}")
        response = self.client.get()

        self.assertTemplateUsed(response=response, template_name='exception_handling/404.html')

    def test_access_created_profile__expect_correct_template(self):
        user = UserModel.objects.create_user(
            **self.VALID_USER_CREDENTIALS
        )
        profile = Profile.objects.create(
            **self.VALID_PROFILE_DATA,
            user=user,
        )

        self.client.get()
        self.assertTemplateUsed('manage_profiles/user/profile.html')

    def test_edit_other_users_profiles__expect_403(self):
        user, profile = self.__create_valid_user_profile()
        self.client.login(**self.VALID_USER_CREDENTIALS)

        different_user = UserModel.objects.create_user(
            email='softunitest2@gmail.com',
            nickname='softunitest2',
            password='SoFtUnTeSt2',
        )
        different_profile = Profile.objects.create(
            **self.VALID_PROFILE_DATA,
            user=different_user,
        )

        response = self.client.get()

        self.assertTemplateUsed(response=response, template_name='exception_handling/403.html')

    def test_edit_other_profiles_with_staff_rights__expect_200(self):
        staff_group = self.__create_valid_staff_group(
            change_profiles_info=True,
        )
        user, profile = self.__create_valid_user_profile(staff_group=staff_group)
        different_user, different_profile = self.__create_valid_user_profile(different=True)

        self.client.login(**self.VALID_USER_CREDENTIALS)

        response = self.client.get()

        self.assertEqual(200, response.status_code)
