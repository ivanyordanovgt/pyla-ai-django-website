from django.contrib.auth import get_user_model
from django.db import models

# Create your models here.
from pyla.manage_profiles.models import ContactUs

UserModel = get_user_model()


class FeedbackReply(models.Model):
    TITLE_MAX_LENGTH = 15

    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
    )

    feedback = models.ForeignKey(
        ContactUs,
        on_delete=models.CASCADE,
    )

    title = models.CharField(
        max_length=TITLE_MAX_LENGTH,
    )

    description = models.TextField()

    tag_other_staff = models.TextField(
        blank=True,
        null=True,
    )

    date = models.DateTimeField(
        auto_now_add=True,
    )
