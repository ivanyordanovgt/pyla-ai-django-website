from django import test as django_test
from django.contrib.auth import get_user_model, login
from django.urls import reverse

from pyla.administrate.models import StaffGroup
from pyla.forums.models import Forum, Post, Comment
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

    def __create_valid_forum(self):
        forum = Forum.objects.create(
            title='SOME FORUM TITLE',
            description='SOME DESCRIPTION',
        )
        return forum

    def __create_valid_post(self, forum_id, user_id):
        post = Post.objects.create(
            title='TEST POST !!!!!!!',
            description='TEST POST DESCRIPTION MUST HAVE SOME LENGTH',
            forum_id=forum_id,
            user_id=user_id,
        )

        return post

    def test_opening_a_valid_forum_expect__200(self):
        forum = self.__create_valid_forum()
        user, profile = self.__create_valid_user_profile()
        self.client.login(**self.VALID_USER_CREDENTIALS)
        response = self.client.get()

        self.assertEqual(200, response.status_code)

    def test_opening_a_valid_post_expect_200(self):
        forum = self.__create_valid_forum()
        user, profile = self.__create_valid_user_profile()
        post = self.__create_valid_post(forum_id=forum.pk, user_id=user.pk)
        self.client.login(**self.VALID_USER_CREDENTIALS)

        response = self.client.get()

        self.assertEqual(200, response.status_code)

    def test_editing_someones_post_expect__correct_template(self):
        forum = self.__create_valid_forum()
        user, profile = self.__create_valid_user_profile()
        user2, profile2 = self.__create_valid_user_profile(different=True)
        post = self.__create_valid_post(forum_id=forum.pk, user_id=user2.pk)
        self.client.login(**self.VALID_USER_CREDENTIALS)

        response = self.client.get()

        self.assertTemplateUsed('exception_handling/403.html')

    def test_deleting_someones_post_expect__correct_template(self):
        forum = self.__create_valid_forum()
        user, profile = self.__create_valid_user_profile()
        user2, profile2 = self.__create_valid_user_profile(different=True)
        post = self.__create_valid_post(forum_id=forum.pk, user_id=user2.pk)
        self.client.login(**self.VALID_USER_CREDENTIALS)

        response = self.client.get()

        self.assertTemplateUsed('exception_handling/403.html')

    def test_editing_own_post__expect_200(self):
        forum = self.__create_valid_forum()
        user, profile = self.__create_valid_user_profile()
        post = self.__create_valid_post(forum_id=forum.pk, user_id=user.pk)
        self.client.login(**self.VALID_USER_CREDENTIALS)
        response = self.client.get()

        self.assertEqual(200, response.status_code)

    def test_delete_own_post__expect_200(self):
        forum = self.__create_valid_forum()
        user, profile = self.__create_valid_user_profile()
        post = self.__create_valid_post(forum_id=forum.pk, user_id=user.pk)
        self.client.login(**self.VALID_USER_CREDENTIALS)
        response = self.client.get()

        self.assertEqual(200, response.status_code)

    def test_edit_other_post_with_rights__except_200(self):
        staff_group = self.__create_valid_staff_group(
            edit_posts=True,
        )
        forum = self.__create_valid_forum()
        user, profile = self.__create_valid_user_profile(staff_group=staff_group)
        user2, profile2 = self.__create_valid_user_profile(different=True)
        post = self.__create_valid_post(forum_id=forum.pk, user_id=user2.pk)
        self.client.login(**self.VALID_USER_CREDENTIALS)
        response = self.client.get()

        self.assertEqual(200, response.status_code)

    def test_delete_other_post_with_rights__except_200(self):
        staff_group = self.__create_valid_staff_group(
            edit_posts=True,
        )
        forum = self.__create_valid_forum()
        user, profile = self.__create_valid_user_profile(staff_group=staff_group)
        user2, profile2 = self.__create_valid_user_profile(different=True)
        post = self.__create_valid_post(forum_id=forum.pk, user_id=user2.pk)
        self.client.login(**self.VALID_USER_CREDENTIALS)
        response = self.client.get()

        self.assertEqual(200, response.status_code)
