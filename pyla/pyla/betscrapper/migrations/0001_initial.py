# Generated by Django 4.0.3 on 2022-04-22 11:28

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BetMatch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bookmaker', models.CharField(max_length=100)),
                ('sport', models.CharField(max_length=100)),
                ('date', models.CharField(max_length=20)),
                ('time', models.CharField(max_length=20)),
                ('match_one', models.CharField(max_length=100)),
                ('match_two', models.CharField(max_length=100)),
                ('bet_type', models.CharField(max_length=100)),
                ('odds', models.CharField(max_length=50)),
                ('liga', models.CharField(max_length=100)),
            ],
        ),
    ]