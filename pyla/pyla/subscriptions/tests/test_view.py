from django import test as django_test
from django.contrib.auth import get_user_model, login
from django.urls import reverse

from pyla.administrate.models import StaffGroup
from pyla.manage_profiles.models import Profile

UserModel = get_user_model()