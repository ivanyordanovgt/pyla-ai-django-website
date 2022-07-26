from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.core.exceptions import PermissionDenied

from pyla.forums.models import Post


class PostCRUDMixin(LoginRequiredMixin, UserPassesTestMixin):

    def test_func(self):
        post = Post.objects.get(pk=self.kwargs['pk'])

        if self.request.user.profile.staff_group:
            if self.request.user.profile.staff_group.edit_posts:
                return True

        if post.user_id == self.request.user.pk:
            return True

        raise PermissionDenied
