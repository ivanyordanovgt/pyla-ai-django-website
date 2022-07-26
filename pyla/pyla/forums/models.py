from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator
from django.db import models

# Create your models here.
from pyla.manage_profiles.models import AppUser

UserModel = get_user_model


class Forum(models.Model):
    TITLE_MAX_LENGTH = 30
    DESCRIPTION_MAX_LENGTH = 800
    title = models.CharField(
        max_length=TITLE_MAX_LENGTH
    )
    description = models.TextField(max_length=DESCRIPTION_MAX_LENGTH)

    date = models.DateTimeField(
        auto_now_add=True,
    )

    image = models.TextField()

    def __str__(self):
        return self.title


class Post(models.Model):
    TITLE_MAX_LENGTH = 45
    TITLE_MIN_LENGTH = 15
    DESCRIPTION_MAX_LENGTH = 600
    DESCRIPTION_MIN_LENGTH = 30
    forum = models.ForeignKey(
        Forum,
        on_delete=models.CASCADE,
    )

    user = models.ForeignKey(
        AppUser,
        on_delete=models.CASCADE,
    )

    title = models.CharField(max_length=TITLE_MAX_LENGTH,
                             validators=(
                                 MinLengthValidator(TITLE_MIN_LENGTH),
                             )
                             )
    description = models.TextField(max_length=DESCRIPTION_MAX_LENGTH,
                                   validators=(
                                       MinLengthValidator(DESCRIPTION_MIN_LENGTH),
                                               )
                                   )
    date = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return self.title


class Comment(models.Model):
    DESCRIPTION_MAX_LENGTH = 200
    DESCRIPTION_MIN_LENGTH = 15
    user = models.ForeignKey(
        AppUser,
        on_delete=models.CASCADE,
    )

    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
    )


    description = models.TextField(max_length=DESCRIPTION_MAX_LENGTH,
                                   validators=(
                                       MinLengthValidator(DESCRIPTION_MIN_LENGTH),
                                              )
                                   )
    date = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return self.description[0:10]
