# Generated by Django 4.1.3 on 2022-12-14 13:01

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_customermessage'),
    ]

    operations = [
        migrations.AddField(
            model_name='coach',
            name='joined_at',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2022, 12, 14, 13, 1, 36, 3602, tzinfo=datetime.timezone.utc)),
            preserve_default=False,
        ),
    ]