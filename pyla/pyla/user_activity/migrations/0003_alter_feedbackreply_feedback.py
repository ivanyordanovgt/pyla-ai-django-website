# Generated by Django 4.0.3 on 2022-04-09 13:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_activity', '0002_feedbackreply_feedback'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedbackreply',
            name='feedback',
            field=models.IntegerField(),
        ),
    ]