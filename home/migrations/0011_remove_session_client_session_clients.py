# Generated by Django 4.1.3 on 2022-11-19 10:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0010_session_duration_session_group_session'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='session',
            name='client',
        ),
        migrations.AddField(
            model_name='session',
            name='clients',
            field=models.ManyToManyField(to='home.client'),
        ),
    ]