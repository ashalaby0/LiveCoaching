# Generated by Django 4.1.3 on 2022-11-15 16:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_alter_coach_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coach',
            name='photo',
            field=models.ImageField(blank=True, upload_to=''),
        ),
    ]
