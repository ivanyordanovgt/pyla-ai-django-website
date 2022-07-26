from django.db import models


# Create your models here.

class Features(models.Model):
    NAME_MAX_LENGTH = 15
    name = models.CharField(max_length=NAME_MAX_LENGTH)
    boolean_choices = (False, True)
    boolean_choices = [(x, x) for x in boolean_choices]

    ESP = models.BooleanField(
        default=False,
    )

    custom_ESP = models.BooleanField(
        default=False,
    )

    lines = models.BooleanField(
        default=False,
    )

    stats_calculator = models.BooleanField(
        default=False,
    )

    match_up_calculator = models.BooleanField(
        default=False,
    )

    autoplay = models.BooleanField(
        default=False,
    )

    complete_quests = models.BooleanField(
        default=False,
    )

    advanced_in_depth_gameplay = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return self.name


class Subscription(models.Model):
    TITLE_MAX_LENGTH = 15

    title = models.CharField(
        max_length=TITLE_MAX_LENGTH,
        unique=True,

    )

    picture = models.ImageField(
        blank=True,
        null=True,

    )

    description = models.TextField()

    features = models.ForeignKey(
        Features,
        on_delete=models.DO_NOTHING,
    )


    def __str__(self):
        return self.title


class TestSubscription(models.Model):
    test = models.CharField(max_length=1)
