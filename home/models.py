import datetime
import json
from time import time
from django.db.models.functions import TruncMonth, Length
from django.db.models import Count



import jwt
import requests
from creditcards.models import (CardExpiryField, CardNumberField,
                                SecurityCodeField)
from django.conf import settings
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


from django.contrib.auth.models import AbstractUser


# TODO
# coach location filed options

class User(AbstractUser):
    phone = models.CharField(max_length=20)

# make the email required for any user
User._meta.get_field('email').blank = False
User._meta.get_field('email').null = False

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.name

class ClientCustomManager(models.QuerySet):

    def get_monthly_stats(self):
        return self.annotate(month=TruncMonth('joined_at')).values('month').annotate(count=Count('id')).values('joined_at__month', 'count')

    def get_total_session_per_client(self):
        return self.annotate(no_of_session=Count('session')).values('user__username', 'no_of_session').order_by('no_of_session')
        # return self.all().values('client').annotate(count=Count('id')).values('client__user__username', 'count')

class Client(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone_number = PhoneNumberField(default="not-provided")
    city = models.CharField(max_length=50, default="not-provided")
    country = models.CharField(max_length=50, default="not-provided")
    joined_at = models.DateTimeField(auto_now_add=True)
    
    objects = ClientCustomManager.as_manager()

    def __str__(self) -> str:
        return self.user.username


class CoachCustomManager(models.QuerySet):

    def get_monthly_stats(self):
        return self.annotate(month=TruncMonth('joined_at')).values('month').annotate(count=Count('id')).values('joined_at__month', 'count')

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

            # execluding last half hour as the duration is 1 hour
            all_half_hours = (
                _date + datetime.timedelta(minutes=i/60) for i in range(0, total_duration, 60*30))

            formated_half_hours = [x.strftime('%H:%M') for x in all_half_hours][:-1]
            for i in coach.session_set.filter(time__date=_date):
                # remove reserved hour from all_half_hours
                if i.time.strftime('%H:%M') in formated_half_hours:
                    # remove current half hour
                    formated_half_hours.remove(i.time.strftime('%H:%M'))
                    
                     # remove next half hour
                    try:
                        formated_half_hours.remove(
                            (i.time + datetime.timedelta(minutes=30)).strftime('%H:%M')) 
                    except:
                        pass

                    # remove previous half hour
                    try:
                        formated_half_hours.remove(
                            (i.time - datetime.timedelta(minutes=30)).strftime('%H:%M')) 
                    except:
                        pass

            return formated_half_hours
        return []


class Coach(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    speciality = models.ForeignKey(Category, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0, validators=[
                                 MaxValueValidator(5), MinValueValidator(0)])
    location = models.CharField(max_length=150, default='Egypt')
    price_per_hour = models.IntegerField(default=0) # in 100 cents
    price_per_30_mins = models.IntegerField(default=0) # in 100 cents
    available_for_kids = models.BooleanField(default=False)
    photo = models.ImageField(upload_to='photo/%Y/%m/%d', blank=True)
    working_hours_start = models.TimeField(default=datetime.time(8, 0, 0))
    working_hours_end = models.TimeField(default=datetime.time(16, 0, 0))
    joined_at = models.DateTimeField(auto_now_add=True)

    objects = CoachCustomManager.as_manager()

    def __str__(self) -> str:
        return self.user.username

class SessionCustomManager(models.QuerySet):

    def get_monthly_stats(self):
        return self.annotate(month=TruncMonth('time')).values('month').annotate(count=Count('id')).values('time__month', 'count')

    def generate_zoom_token(self):
        API_KEY = settings.ZOOM_API_KEY
        API_SEC = settings.ZOOM_API_SEC
        token = jwt.encode(
            {'iss': API_KEY, 'exp': time() + 5000},
            API_SEC,
            algorithm='HS256'
        )
        return jwt.decode(token, API_SEC, algorithms=["HS256"])

    def get_upcomming_sessions(self):
        return self.filter(time__gte=datetime.datetime.now())

    def get_total_session_per_coach(self):
        return self.all().values('coach').annotate(count=Count('id')).values('coach__user__username', 'count').order_by('count')

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
    meeting = models.ForeignKey('ZoomMeeting', on_delete=models.CASCADE, null=True, blank=True)
    # url = models.URLField(default=None, null=True)

    objects = SessionCustomManager.as_manager()

    def __str__(self) -> str:
        return f'{self.category}: {self.coach}'


class Order(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    item = models.ForeignKey(Session, on_delete=models.CASCADE)
    ordered_date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.client.user.username

class CustomerMessage(models.Model):
    full_name = models.CharField(max_length=50)
    email = models.EmailField()
    message = models.TextField()
    phone_number = PhoneNumberField(blank=True, null=True)
    closed = models.BooleanField(default=False)

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
        print(token)
        if token:
            return True, token
        return False, token

    def _paymob_seccond_api_call(
        self, 
        token, 
        merchant_order_id,
        amount_cents,
        item_name,
        quantity,
        email,
        first_name,
        last_name,
        phone_number,
        city,
        country
        ):
        url = 'https://accept.paymob.com/api/ecommerce/orders'
        merchant_order_id += 2000 # for testing
        print(merchant_order_id)
        context = {
            "auth_token":  token,
            "delivery_needed": "false",
            "amount_cents": amount_cents,
            "currency": "EGP",
            "merchant_order_id": merchant_order_id,
            "items": [
                {
                    "name": item_name,
                    "amount_cents": amount_cents,
                    "description": item_name,
                    "quantity": quantity
                }
            ],
            "shipping_data": {
                "apartment": "",
                "email": email,
                "floor": "",
                "first_name": first_name,
                "street": "",
                "building": "",
                "phone_number": phone_number,
                "postal_code": "",
                "extra_description": "",
                "city": city,
                "country": country,
                "last_name": last_name,
                "state": ""
            },
            "shipping_details": {
                "notes": "",
                "number_of_packages": 1,
                "weight": 1,
                "weight_unit": "Kilogram",
                "length": 1,
                "width": 1,
                "height": 1,
                "contents": ""
            }
        }

        r = requests.post(url, json=context)
        print(r.json())
        id = r.json().get('id')
        msg = r.json().get('message')
        if not id:
            return False, msg
        return True, id

    def _paymob_third_api_call(
        self, 
        token, 
        order_id, 
        integration_id,
        first_name,
        last_name,
        email,
        phone_number,
        city,
        country,
        amount_cents,
        state=None,
        building=None,
        apartment=None,
        street=None,
        postal_code=None,
        floor=None
        ):

        if not state:
            state = 'not-provided'

        if not building:
            building = 'not-provided'

        if not apartment:
            apartment = 'not-provided'

        if not street:
            street = 'not-provided'

        if not postal_code:
            postal_code = 'not-provided'

        if not floor:
            floor = 'not-provided'
            
        url = 'https://accept.paymob.com/api/acceptance/payment_keys'

        billing_data = {
            "apartment": apartment,
            "email": email,
            "floor": floor,
            "first_name": first_name,
            "street": street,
            "building": building,
                        "phone_number": phone_number,
                        "shipping_method": "",
                        "postal_code": postal_code,
                        "city": city,
                        "country": country,
                        "last_name": last_name,
                        "state": state
        }
        context = {
            "auth_token": token,
            "amount_cents": amount_cents,
            "expiration": 3600,
            "order_id": order_id,
            "billing_data": billing_data,
            "currency": "EGP",
            "integration_id": integration_id,
            "lock_order_when_paid": "false"
        }

        r = requests.post(url, json=context)
        token = r.json().get('token')
        print(r.json())
        if not token:
            return False, token
        return True,  token

    def get_paymob_token(
        self, 
        merchant_order_id,
        coach,
        client
        ):

        if not client.user.first_name:
            first_name = 'not-provided'
        else:
            first_name = client.user.first_name

        if not client.user.last_name:
            last_name = 'not-provided'
        else:
            last_name = client.user.last_name

        if not client.user.email:
            email = 'not-provided'
        else:
            email = client.user.email

        if not client.city:
            city = 'not-provided'
        else:
            city = client.city

        if not client.country:
            country = 'not-provided'
        else:
            country = client.country

        integration_id = settings.PAYMOB_INTEGRATION_ID
        result = self._paymob_first_api_call()
        if not result[0]:
            return result
        token = result[1]

        result = self._paymob_seccond_api_call(
            token=token, 
            merchant_order_id=merchant_order_id,
            amount_cents=coach.price_per_hour * 100,
            item_name=coach.speciality.name,
            quantity=1,
            email=email,
            first_name=first_name,
            last_name=last_name,
            phone_number=str(client.phone_number),
            city=city,
            country=country
            )

        if not result[0]:
            return result
        order_id = result[1]

        return self._paymob_third_api_call(
            token, 
            order_id, 
            integration_id,
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone_number=str(client.phone_number),
            city=city,
            country=country,
            amount_cents=coach.price_per_hour * 100

            )


class ZoomMeetingCustomManager(models.QuerySet):
    def upcomming_meetings(self, _user):
        return self.filter(start_time__gte=datetime.datetime.now())
class ZoomMeeting(models.Model):
    join_url = models.URLField()
    start_url = models.URLField()
    meeting_id = models.IntegerField()
    start_time = models.DateTimeField()
    duration = models.IntegerField()

    objects = ZoomMeetingCustomManager.as_manager()


