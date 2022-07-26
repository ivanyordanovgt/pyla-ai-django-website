from django.db import models


# Create your models here.

class Category(models.Model):
    NAME_MAX_LEN = 20
    name = models.CharField(max_length=NAME_MAX_LEN)


class Todo(models.Model):
    TITLE_MAX_LEN = 14
    title = models.CharField(max_length=TITLE_MAX_LEN)

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,

    )


class AAATodo(models.Model):
    harisjhaiodufjgsfoig = models.TextField()
