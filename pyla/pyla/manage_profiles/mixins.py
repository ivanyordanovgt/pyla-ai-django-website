from abc import ABC

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied


class CRUDAccessMixin(UserPassesTestMixin):

    def test_func(self):
        if self.request.user.is_authenticated:

            if self.request.user.is_staff:
                return True

            if self.request.user.pk == self.kwargs['pk']:
                return True


class FullCRUDProfileMixin(UserPassesTestMixin):

    def test_func(self):

        if self.request.user.pk == self.kwargs['pk']:
            return True

        else:
            if self.request.user.profile.staff_group:
                if self.request.user.profile.staff_group.change_profiles_info:
                    return True
            return False

