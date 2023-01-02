# Generated by Django 4.1.3 on 2022-12-30 17:24

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PromoCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('valid', models.BooleanField(default=True)),
                ('code', models.CharField(blank=True, max_length=50, null=True)),
                ('used_by', models.ManyToManyField(to='home.client')),
            ],
        ),
    ]