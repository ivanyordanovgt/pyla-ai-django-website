from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import ValidationError, PermissionDenied
from django.http import HttpResponseNotFound


class StaffMixin(UserPassesTestMixin):

    def test_func(self):
        if self.request.user.profile.staff_group:
            return True


class HandleFeedbackMixin(UserPassesTestMixin):
    def test_func(self):

        try:
            if self.request.user.profile.staff_group.response_to_feedback:
                return True
        except AttributeError:
            raise PermissionDenied()


class ConfigureIndexMixin(UserPassesTestMixin):
    def test_func(self):


        try:
            if self.request.user.profile.staff_group.edit_index:
                return True
        except AttributeError:
            return PermissionDenied()

class ConfigureAboutPageMixin(UserPassesTestMixin):
    def test_func(self):

        try:
            if self.request.user.profile.staff_group.edit_about_page:
                return True

        except AttributeError:
            raise PermissionDenied()


class CreateSubscriptionMixin(UserPassesTestMixin):
    def test_func(self):

        try:
            if self.request.user.profile.staff_group.create_subscription:
                return True
        except AttributeError:
            raise PermissionDenied()
