from django import template

register = template.Library()


@register.filter(name='rework')
def rework(value):  # Only one argument.
    """Converts a string into all lowercase"""
    return " ".join(value.split("_"))


@register.filter(name='feature_selector')
def feature_selector(value, title):
    for feature_title, features in value.items():
        if feature_title == title:
            return features


@register.filter(name='boolean_to_status')
def boolean_to_status(value):  # Only one argument.

    if value:
        return "Handled"
    return "In progress"
