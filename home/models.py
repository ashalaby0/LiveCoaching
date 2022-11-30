import datetime
import json
from time import time

import jwt
import requests
from creditcards.models import (CardExpiryField, CardNumberField,
                                SecurityCodeField)
from django.conf import settings
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

# TODO
# coach location filed options


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.name


class Client(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.user.username


class CoachCustomManager(models.QuerySet):
    # def get_available_hours(self, pk, _date):
    #     coach_list = self.filter(pk=pk)
    #     if coach_list.count() > 0:
    #         coach = coach_list[0]
    #         all_hours = set(range(coach.working_hours_start.hour,
    #                               coach.working_hours_end.hour))
    #         for i in coach.session_set.all():
    #             print(i.time.hour)
    #             if i.time.hour in all_hours:
    #                 all_hours.remove(i.time.hour)

    #         all_hours = [
    #             datetime.time(x, 0, 0).strftime('%H:%M') for x in all_hours
    #         ]
    #         return all_hours
    #     return []

    def get_available_hours(self, pk, day):
        coach_list = self.filter(pk=pk)
        if coach_list.count() > 0:
            coach = coach_list[0]
            _date = datetime.datetime.combine(datetime.date(
                *[int(x) for x in day.split('-')]), coach.working_hours_start)

            total_duration = (
                datetime.datetime.combine(datetime.date.today(
                ), coach.working_hours_end) - datetime.datetime.combine(datetime.date.today(), coach.working_hours_start)
            ).seconds
            all_half_hours = (
                _date + datetime.timedelta(minutes=i/60) for i in range(0, total_duration, 60*30))

            formated_half_hours = [x.strftime('%H:%M') for x in all_half_hours]
            for i in coach.session_set.filter(time__date=_date):
                # remove reserved hour from all_half_hours
                if i.time.strftime('%H:%M') in formated_half_hours:
                    # remove current half hour
                    formated_half_hours.remove(i.time.strftime('%H:%M'))
                    formated_half_hours.remove(
                        (i.time + datetime.timedelta(minutes=30)).strftime('%H:%M'))  # remove next half hour

            # formated_half_hours = [x.strftime('%H:%M') for x in formated_half_hours]
            return formated_half_hours
        return []


class Coach(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    speciality = models.ForeignKey(Category, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0, validators=[
                                 MaxValueValidator(5), MinValueValidator(0)])
    location = models.CharField(max_length=150, default='Egypt')
    price_per_hour = models.IntegerField(default=0)
    price_per_30_mins = models.IntegerField(default=0)
    available_for_kids = models.BooleanField(default=False)
    photo = models.ImageField(upload_to='photo/%Y/%m/%d', blank=True)
    working_hours_start = models.TimeField(default=datetime.time(8, 0, 0))
    working_hours_end = models.TimeField(default=datetime.time(16, 0, 0))

    objects = CoachCustomManager.as_manager()

    def __str__(self) -> str:
        return self.user.username

# not used


class SessionCustomManager(models.QuerySet):

    def generate_zoom_token(self):
        API_KEY = settings.ZOOM_API_KEY
        API_SEC = settings.ZOOM_API_SEC
        token = jwt.encode(
            {'iss': API_KEY, 'exp': time() + 5000},
            API_SEC,
            algorithm='HS256'
        )
        return jwt.decode(token, API_SEC, algorithms=["HS256"])

    def create_zoom_meeting(self, topic, start_time, duration_in_mins, time_zone, agenda):
        formated_time = '2022-12-12T11: 11: 11'  # will be formated from start_time
        payload = {
            "topic": topic,
            "type": 2,
            "start_time": formated_time,
            "duration": duration_in_mins,
            "timezone": time_zone,
            "agenda": agenda,

            "recurrence": {"type": 1,
                           "repeat_interval": 1
                           },
            "settings": {"host_video": "true",
                         "participant_video": "true",
                         "join_before_host": "False",
                         "mute_upon_entry": "True",
                         "watermark": "true",
                         "audio": "voip",
                         "auto_recording": "cloud"
                         }
        }

        headers = {
            'authorization': f'Bearer {self.generate_zoom_token()}',
            'content/type': 'application/json'
        }

        response = requests.post(
            settings.ZOOM_API_URL,
            headers=headers,
            data=json.dumps(payload)
        )

        result = response.json()
        print(result)


class Session(models.Model):
    clients = models.ManyToManyField(Client)
    coach = models.ForeignKey(Coach, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    time = models.DateTimeField()
    duration = models.IntegerField(default=60)
    review = models.CharField(max_length=500, default='')
    group_session = models.BooleanField(default=False)
    url = models.URLField(default=None, null=True)

    # objects = SessionCustomManager.as_manager()

    def __str__(self) -> str:
        return f'{self.category}: {self.coach}'


class Order(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    item = models.ForeignKey(Session, on_delete=models.CASCADE)
    ordered_date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.client.user.username


class Payment(models.Model):
    shipment_address = models.CharField(max_length=150)
    chipment_phone = models.CharField(max_length=150)
    card_number = CardNumberField()
    expiry_date = CardExpiryField()
    security_code = SecurityCodeField()

    def _paymob_first_api_call(self):
        url = 'https://accept.paymob.com/api/auth/tokens'
        context = {"api_key": "ZXlKaGJHY2lPaUpJVXpVeE1pSXNJblI1Y0NJNklrcFhWQ0o5LmV5SnVZVzFsSWpvaWFXNXBkR2xoYkNJc0luQnliMlpwYkdWZmNHc2lPall5TURFd05Dd2lZMnhoYzNNaU9pSk5aWEpqYUdGdWRDSjkuNFpXTDFTemZfWC1FUEowcUtldXZ1VVN0WlJrU1dNNm0zRXFGZFlzNlZvS3ZZaEFBcFpSMGg1cURvVkNIZkd2MWFJUWFBSWRJbjZZaFlmejJwMkdqdEE="}
        r = requests.post(url, json=context)
        token = r.json().get('token')
        if token:
            return True, token
        return False, token

    def _paymob_seccond_api_call(self, token, merchant_order_id):
        url = 'https://accept.paymob.com/api/ecommerce/orders'
        context = {
            "auth_token":  token,
            "delivery_needed": "false",
            "amount_cents": "100",
            "currency": "EGP",
            "merchant_order_id": merchant_order_id,
            "items": [
                {
                    "name": "ASC1515",
                    "amount_cents": "500000",
                    "description": "Smart Watch",
                    "quantity": "1"
                },
                {
                    "name": "ERT6565",
                    "amount_cents": "200000",
                    "description": "Power Bank",
                    "quantity": "1"
                }
            ],
            "shipping_data": {
                "apartment": "803",
                "email": "claudette09@exa.com",
                "floor": "42",
                "first_name": "Clifford",
                "street": "Ethan Land",
                "building": "8028",
                "phone_number": "+86(8)9135210487",
                "postal_code": "01898",
                "extra_description": "8 Ram , 128 Giga",
                "city": "Jaskolskiburgh",
                "country": "CR",
                "last_name": "Nicolas",
                "state": "Utah"
            },
            "shipping_details": {
                "notes": " test",
                "number_of_packages": 1,
                "weight": 1,
                "weight_unit": "Kilogram",
                "length": 1,
                "width": 1,
                "height": 1,
                "contents": "product of some sorts"
            }
        }

        r = requests.post(url, json=context)
        id = r.json().get('id')
        msg = r.json().get('message')
        if not id:
            return False, msg
        return True, id

    def _paymob_third_api_call(self, token, order_id, integration_id):
        url = 'https://accept.paymob.com/api/acceptance/payment_keys'

        billing_data = {
            "apartment": "803",
            "email": "claudette09@exa.com",
            "floor": "42",
            "first_name": "Clifford",
            "street": "Ethan Land",
            "building": "8028",
                        "phone_number": "+86(8)9135210487",
                        "shipping_method": "PKG",
                        "postal_code": "01898",
                        "city": "Jaskolskiburgh",
                        "country": "CR",
                        "last_name": "Nicolas",
                        "state": "Utah"
        }
        context = {
            "auth_token": token,
            "amount_cents": "100",
            "expiration": 3600,
            "order_id": order_id,
            "billing_data": billing_data,
            "currency": "EGP",
            "integration_id": integration_id,
            "lock_order_when_paid": "false"
        }

        r = requests.post(url, json=context)
        token = r.json().get('token')
        if not token:
            return False, token
        return True,  token

    def get_paymob_token(self, merchant_order_id):
        integration_id = '3065725'
        result = self._paymob_first_api_call()
        if not result[0]:
            return result
        token = result[1]

        result = self._paymob_seccond_api_call(
            token=token, merchant_order_id=merchant_order_id)
        if not result[0]:
            return result
        order_id = result[1]

        return self._paymob_third_api_call(token, order_id, integration_id)
