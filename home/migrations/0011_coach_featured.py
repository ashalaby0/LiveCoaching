# Generated by Django 4.1.3 on 2023-01-01 22:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0010_coach_brief'),
    ]

    operations = [
        migrations.AddField(
            model_name='coach',
            name='featured',
            field=models.BooleanField(default=False),
        ),
    ]