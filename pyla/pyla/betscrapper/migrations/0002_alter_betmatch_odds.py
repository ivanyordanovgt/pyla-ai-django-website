# Generated by Django 4.0.3 on 2022-04-23 13:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('betscrapper', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='betmatch',
            name='odds',
            field=models.FloatField(),
        ),
    ]