from django.core.validators import MinLengthValidator
from django.db import models

# Create your models here.
from pyla.web.validators import disable_editing


class Task(models.Model):
    text = models.TextField()


class IndexConfigurator(models.Model):
    NAME = "Index configurator"
    MAX_PYLA_MOTO_LENGTH = 70
    MIN_PYLA_MOTO_LENGTH = 5
    pyla_moto = models.TextField(
        max_length=MAX_PYLA_MOTO_LENGTH,
        validators=(MinLengthValidator(MIN_PYLA_MOTO_LENGTH),)
    )

    pyla_img = models.ImageField(
        blank=True,
        null=True,
        validators=(
            disable_editing,
        )
    )

    def __str__(self):
        return f"{self.NAME}"


class AboutPylaPageConfigurator(models.Model):
    CONFIGURATORNAME = 'About Pyla configurator'

    about_pyla_text = models.TextField()
    goals_text = models.TextField()

    def __str__(self):
        return f"{self.CONFIGURATORNAME}"


class AboutPylaTextConfigurator(models.Model):
    CONFIGURATOR_NAME = 'About Pyla configurator'

    about_pyla_text = models.TextField()
    goals_text = models.TextField()

    def __str__(self):
        return f"{self.CONFIGURATOR_NAME}"


