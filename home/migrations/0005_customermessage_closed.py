# Generated by Django 4.1.3 on 2022-12-15 20:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_client_joined_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='customermessage',
            name='closed',
            field=models.BooleanField(default=False),
        ),
    ]