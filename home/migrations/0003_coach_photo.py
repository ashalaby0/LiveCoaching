# Generated by Django 4.1.3 on 2022-11-15 15:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_coach_available_for_kids_coach_location_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='coach',
            name='photo',
            field=models.ImageField(blank=True, upload_to=''),
        ),
    ]