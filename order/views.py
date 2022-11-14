from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import hmac
import hashlib

from . import models


def payment_view(request):
    """ payment wity paymob 
    
        - send 3 apis to paymob to get token.
        - if succeeded to get token:
            - redirect to paymob iframe to pay.
            - validate payment with paymob and display result to client
        - if failed
            - display failure alert.
    """
    new_order = models.Order(name='newOrder', user=request.user)
    new_order.save()
    merchant_order_id = new_order.id
    payment = models.Payment()
    status, payment_key = payment.get_paymob_token(merchant_order_id=merchant_order_id)

    
    if status:
        iframe_page = f'https://accept.paymob.com/api/acceptance/iframes/698300?payment_token={payment_key}'
        return HttpResponseRedirect(iframe_page)
    
    result = 'Payment Failed .. '
    if payment_key == 'duplicate':
        result += "Duplicate Product ID"
    return render(
            request=request,
            template_name='order/result.html',
            context={'result':result, 'status':status}
        )

@csrf_exempt
def post_pay(request):
    """ paymob hmac validation"""

    hmac_secret = 'FDDE8D8FB185CDE6AA6CCF5D5BD8FBD8'
    hmac_fields = [
        'amount_cents',
        'created_at',
        'currency',
        'error_occured',
        'has_parent_transaction',
        'id',
        'integration_id',
        'is_3d_secure',
        'is_auth',
        'is_capture',
        'is_refunded',
        'is_standalone_payment',
        'is_voided',
        'order',
        'owner',
        'pending',
        'source_data.pan',
        'source_data.sub_type',
        'source_data.type',
        'success',
    ]
    hmac_fields.sort()
    result = 'post_request'
    if request.method == 'GET': 
        sent_hmac = request.GET.get('hmac')
        concatenated_str = ''.join(request.GET.get(i) for i in hmac_fields)
        generated_hmac = hmac.new(hmac_secret.encode('utf-8'), concatenated_str.encode('utf8'), hashlib.sha512).hexdigest()
        result = hmac.compare_digest(generated_hmac, sent_hmac)
        return render(
            request=request,
            template_name='order/result.html',
            context={'result':result, 'status': True}
        )
    return HttpResponse(f'<h6>RESULT: {result}</h6>')
    