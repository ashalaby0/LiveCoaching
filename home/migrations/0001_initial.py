# Generated by Django 4.1.3 on 2022-12-13 06:56

import creditcards.models
import datetime
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(default='not-provided', max_length=128, region=None, unique=True)),
                ('city', models.CharField(default='not-provided', max_length=50)),
                ('country', models.CharField(default='not-provided', max_length=50)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Coach',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField(default=0, validators=[django.core.validators.MaxValueValidator(5), django.core.validators.MinValueValidator(0)])),
                ('location', models.CharField(default='Egypt', max_length=150)),
                ('price_per_hour', models.IntegerField(default=0)),
                ('price_per_30_mins', models.IntegerField(default=0)),
                ('available_for_kids', models.BooleanField(default=False)),
                ('photo', models.ImageField(blank=True, upload_to='photo/%Y/%m/%d')),
                ('working_hours_start', models.TimeField(default=datetime.time(8, 0))),
                ('working_hours_end', models.TimeField(default=datetime.time(16, 0))),
                ('speciality', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.category')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shipment_address', models.CharField(max_length=150)),
                ('chipment_phone', models.CharField(max_length=150)),
                ('card_number', creditcards.models.CardNumberField(max_length=25)),
                ('expiry_date', creditcards.models.CardExpiryField()),
                ('security_code', creditcards.models.SecurityCodeField(max_length=4)),
            ],
        ),
        migrations.CreateModel(
            name='Session',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField()),
                ('duration', models.IntegerField(default=60)),
                ('review', models.CharField(default='', max_length=500)),
                ('group_session', models.BooleanField(default=False)),
                ('url', models.URLField(default=None, null=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.category')),
                ('clients', models.ManyToManyField(to='home.client')),
                ('coach', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.coach')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ordered_date', models.DateTimeField(auto_now_add=True)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.client')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.session')),
            ],
        ),
    ]
