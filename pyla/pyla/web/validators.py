from django.core.exceptions import ValidationError


def disable_editing(value):
    if value:
        raise ValidationError("Image is not configured to be edited for now.")
