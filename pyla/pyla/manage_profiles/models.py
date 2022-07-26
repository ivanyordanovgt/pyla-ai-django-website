from django.contrib.auth import models as auth_models
from django.contrib.auth.models import User
from django.db import models
from django import forms

from pyla import settings
from pyla.administrate.models import StaffGroup
from pyla.manage_profiles.managers import AppUsersManager


class AppUser(auth_models.AbstractBaseUser, auth_models.PermissionsMixin):
    NICKNAME_MAX_LENGTH = 25

    email = models.EmailField(
        unique=True,
        null=False,
        blank=False,
    )

    nickname = models.CharField(
        max_length=NICKNAME_MAX_LENGTH,
        blank=False,
        null=False,
        unique=True,
    )

    is_staff = models.BooleanField(
        default=False,
    )

    date_joined = models.DateTimeField(
        auto_now_add=True,
    )

    is_active = models.BooleanField(
        default=True,
    )

    is_activated = models.BooleanField(
        default=False,
    )

    USERNAME_FIELD = 'email'

    objects = AppUsersManager()

    def __str__(self):
        return f"{self.nickname} {self.email}"


class Profile(models.Model):
    DESCRIPTION_MAX_LENGTH = 300
    MOTO_MAX_LENGTH = 50
    description = models.TextField(
        max_length=DESCRIPTION_MAX_LENGTH,
        blank=True,
        null=True,
    )

    profile_picture = models.ImageField(
        blank=True,
        null=True,

    )

    moto = models.CharField(
        max_length=MOTO_MAX_LENGTH,
        null=True,
        blank=True,
    )

    user = models.OneToOneField(
        AppUser,
        on_delete=models.CASCADE,
        primary_key=True,
    )

    staff_group = models.ForeignKey(
        StaffGroup,
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
    )

    balance = models.IntegerField(
        default=120,
    )

    def __str__(self):
        return self.user.nickname


user = settings.AUTH_USER_MODEL


class ContactUs(models.Model):
    TITLE_MAX_LENGTH = 30

    user = models.ForeignKey(
        user,
        on_delete=models.CASCADE,
    )

    title = models.CharField(
        max_length=TITLE_MAX_LENGTH,
    )

    image = models.ImageField(
        blank=True,
        null=True,

    )

    video = models.URLField(
        blank=True,
        null=True,
    )

    description = models.TextField()

    status = models.BooleanField(
        default=False,
    )

    def __str__(self):
        if self.status:
            return "Handled"
        return f"{self.title} ---> {self.user.nickname} ---> {self.pk}"


class ChangePasswordKeys(models.Model):
    security_key = models.TextField()
    email = models.EmailField()
    date = models.DateTimeField(
        auto_now_add=True,
    )


class EmailKey(models.Model):

    security_key = models.TextField()
    user = models.ForeignKey(
        AppUser,
        on_delete=models.CASCADE,
    )

    date = models.DateTimeField(
        auto_now_add=True,
    )