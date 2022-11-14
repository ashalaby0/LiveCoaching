from django.db import models
from django.contrib.auth.models import User
import requests

from creditcards.models import CardNumberField, CardExpiryField, SecurityCodeField


#TODO
# login .. done
# register .. done
# password reset .. pending
# payment .. test done { pending on read payment test} 
# pages:
    # home page .. in progress
    # coach profile page .. pending
    # client profile page .. pending
    # search .. pending
    # filter .. pending
    
# session
    # start_time
    # status
    # duration
    # coach
    # client_set
    

# client ( extend user mode )
    # name
    # email
    # gender
    # ..
    
# coach ( extend user mode )
    # name
    # speciality
    # rating
    # location
    # price_per_hour
    # price_per_30
    # available_for_kids


class Order(models.Model):
    name  = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_finished = models.BooleanField(default=False)
    price = models.IntegerField(default=0)

class OrderDetails(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

class Payment(models.Model):
    models.ForeignKey(Order, on_delete=models.CASCADE)
    shipment_address  = models.CharField(max_length=150)
    chipment_phone = models.CharField(max_length=150)
    card_number = CardNumberField()
    expiry_date = CardExpiryField()
    security_code = SecurityCodeField()

    def _paymob_first_api_call(self):
        url = 'https://accept.paymob.com/api/auth/tokens'
        context = {"api_key": "ZXlKaGJHY2lPaUpJVXpVeE1pSXNJblI1Y0NJNklrcFhWQ0o5LmV5SnVZVzFsSWpvaWFXNXBkR2xoYkNJc0luQnliMlpwYkdWZmNHc2lPall5TURFd05Dd2lZMnhoYzNNaU9pSk5aWEpqYUdGdWRDSjkuNFpXTDFTemZfWC1FUEowcUtldXZ1VVN0WlJrU1dNNm0zRXFGZFlzNlZvS3ZZaEFBcFpSMGg1cURvVkNIZkd2MWFJUWFBSWRJbjZZaFlmejJwMkdqdEE="}
        r = requests.post(url, json = context)
        token = r.json().get('token')
        print(token)
        if token:
            return True, token
        return False, token
        
    def _paymob_seccond_api_call(self, token, merchant_order_id):
        print(merchant_order_id)
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
                    "notes" : " test",
                    "number_of_packages": 1,
                    "weight" : 1,
                    "weight_unit" : "Kilogram",
                    "length" : 1,
                    "width" :1,
                    "height" :1,
                    "contents" : "product of some sorts"
                }
            }

        r = requests.post(url, json = context)
        id = r.json().get('id')
        msg = r.json().get('message')
        if not id:
            return False, msg
        return True, id

    def _paymob_third_api_call(self, token, order_id, integration_id):
        print('third api 333333333333333')
        url = 'https://accept.paymob.com/api/acceptance/payment_keys'
        print('order_id', order_id)

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

        r = requests.post(url, json = context)
        token = r.json().get('token')
        if not token:
            return False, token
        return True,  token

    def get_paymob_token(self, merchant_order_id):
        """ get paymob token through paymob 3 api calls"""
        integration_id = '3065725'
        result = self._paymob_first_api_call()
        if not result[0]:
            return result
        token = result[1]

        result = self._paymob_seccond_api_call(token=token, merchant_order_id=merchant_order_id)
        if not result[0]:
            return result
        order_id = result[1]

        return self._paymob_third_api_call(token, order_id, integration_id)
