from django.db import models


# Create your models here.

class StaffGroup(models.Model):
    TITLE_MAX_LENGTH = 15
    title = models.CharField(max_length=TITLE_MAX_LENGTH)

    edit_index = models.BooleanField(
        default=False,
    )
    edit_about_page = models.BooleanField(
        default=False,
    )
    edit_subscription = models.BooleanField(
        default=False,
    )
    create_subscription = models.BooleanField(
        default=False,
    )
    response_to_feedback = models.BooleanField(
        default=False,
    )
    change_profiles_info = models.BooleanField(
        default=False,
    )
    change_profile_group = models.BooleanField(
        default=False,
    )
    edit_forums = models.BooleanField(
        default=False,
    )
    create_forums = models.BooleanField(
        default=False,
    )
    edit_posts = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return self.title
