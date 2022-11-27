import base64
import datetime
import hashlib
import hmac

import requests
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView

from . import forms, models


def home(request):
    return render(
        request=request,
        template_name='home/home.html',
        context={}
    )


@login_required(login_url='/accounts/login')
def coaches(request):

    coach_name_q = request.GET.get('coach_name_q') if request.GET.get(
        'coach_name_q') != None else ''
    coach_speciality_q = request.GET.get('coach_speciality_q') if request.GET.get(
        'coach_speciality_q') != None else ''
    min_price_q = request.GET.get('min_price_q') if request.GET.get(
        'min_price_q') != None else 0
    max_price_q = request.GET.get('max_price_q') if request.GET.get(
        'max_price_q') != None else 1000

    available_date_q = request.GET.get('available_date_q') if request.GET.get(
        'available_date_q') != None else ''

    coach_list = models.Coach.objects.filter(
        Q(user__username__icontains=coach_name_q) &
        Q(speciality__name__icontains=coach_speciality_q) &
        Q(price_per_hour__gte=min_price_q) &
        Q(price_per_hour__lte=max_price_q)
    )
    return render(
        request=request,
        template_name='home/coaches.html',
        context={'coach_list': coach_list}
    )


@login_required(login_url='/accounts/login')
def sessions(request):

    coach_name_q = request.GET.get('coach_name_q') if request.GET.get(
        'coach_name_q') != None else ''
    coach_speciality_q = request.GET.get('coach_speciality_q') if request.GET.get(
        'coach_speciality_q') != None else ''
    min_price_q = request.GET.get('min_price_q') if request.GET.get(
        'min_price_q') != None else 0
    max_price_q = request.GET.get('max_price_q') if request.GET.get(
        'max_price_q') != None else 1000

    available_date_q = request.GET.get('available_date_q') if request.GET.get(
        'available_date_q') != None else ''

    if available_date_q:
        _date_q = datetime.datetime.strptime(
            available_date_q, '%Y-%m-%d').date()

        session_list = models.Session.objects.filter(
            Q(coach__user__username__icontains=coach_name_q) &
            Q(coach__speciality__icontains=coach_speciality_q) &
            Q(coach__price_per_hour__gte=min_price_q) &
            Q(coach__price_per_hour__lte=max_price_q) &
            Q(group_session=True) &
            Q(time__date=_date_q)
        )
    else:
        session_list = models.Session.objects.filter(
            Q(coach__user__username__icontains=coach_name_q) &
            Q(coach__speciality__name__icontains=coach_speciality_q) &
            Q(coach__price_per_hour__gte=min_price_q) &
            Q(coach__price_per_hour__lte=max_price_q) &
            Q(group_session=True)
        )
    return render(
        request=request,
        template_name='home/sessions.html',
        context={'session_list': session_list}
    )


def get_coach_available_hours(request, pk):
    hours = models.Coach.objects.get_available_hours(pk)
    return JsonResponse({'av_hours': hours})


def booking(request, pk):
    client, status = models.Client.objects.get_or_create(user=request.user.id)
    print(client)

    coach = get_object_or_404(models.Coach, pk=pk)
    private_session_set = models.Session.objects.filter(
        clients=client.id)
    group_session_set = models.Session.objects.filter(coach__id=pk)

    context = {
        'private_session_set': private_session_set,
        'group_session_set': group_session_set,
        'coach': coach,
        'session_form': forms.SessionModelForm()
    }
    return render(
        request=request,
        template_name='home/booking.html',
        context=context
    )


class CoachDetailView(DetailView):
    model = models.Coach
    template_name = 'home/coach_profile.html'


def schedule_zoom_meeting(request):

    meeting_date = request.POST.get('meeting_date')
    meeting_topic = request.POST.get('meeting_topic')
    meeting_agenda = request.POST.get('meeting_agenda')
    request.session['meeting_date'] = meeting_date
    request.session['meeting_topic'] = meeting_topic
    request.session['meeting_agenda'] = meeting_agenda

    ZOOM_OAUTH_REDIRECT_URL = request.build_absolute_uri(
        reverse(settings.ZOOM_OAUTH_REDIRECT_URL_NAME))
    return redirect(settings.ZOOM_USER_AUTHORIZATON_URL_BASE + ZOOM_OAUTH_REDIRECT_URL)


def zoom_callback(request):
    response = requests.post(
        url=settings.ZOOM_TOKEN_REQUEST_URL,
        headers={
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': 'Basic ' + base64.b64encode(bytes(f'{settings.ZOOM_API_KEY}:{settings.ZOOM_API_SEC}', 'utf-8')).decode('utf-8')
        },
        data={
            'code': request.GET.get('code'),
            'grant_type': 'authorization_code',
            'redirect_uri': request.build_absolute_uri(reverse('zoom_callback'))
        }
    )
    access_token = response.json()['access_token']

    meeting_date = request.session['meeting_date']
    meeting_topic = request.session['meeting_topic']
    meeting_agenda = request.session['meeting_agenda']

    response = requests.post(
        url=settings.ZOOM_MEETING_URL,
        headers={
            'Authorization': 'Bearer ' + access_token,
            'content-type': 'application/json'
        },
        json={
            'agenda': meeting_agenda,
            'default_password': False,
            'duration': settings.ZOOM_MEETING_DURATION,
            'password': settings.ZOOM_MEETING_PASSWORD,
            'pre_schedule': False,
            'schedule_for': request.user.email,
            'schedule_time': meeting_date,
            'timezone': 'Egypt/Cairo',
            'Topic': meeting_topic,
            'type': 2
        }
    )
    return response


def payment_view(request):

    coach_id = request.POST.get('coach_id')
    session_hour = request.POST.get('sessionHour')
    session_hour = int(session_hour.split(':')[0])
    session_date = request.POST.get('session_date')
    _year, _month, _day = session_date.split('-')
    _year = int(_year)
    _month = int(_month)
    _day = int(_day)

    client = models.Client.objects.get(user=request.user)
    _time = datetime.datetime(
        _year, _month, _day, session_hour, 0, 0)
    coach = models.Coach.objects.get(pk=coach_id)
    new_session = models.Session.objects.create(
        coach=coach, time=_time, category=coach.speciality, group_session=False)
    new_session.clients.add(client)

    new_order = models.Order.objects.create(client=client, item=new_session)

    merchant_order_id = new_order.id
    payment = models.Payment()
    status, payment_key = payment.get_paymob_token(
        merchant_order_id=merchant_order_id)

    if status:
        iframe_page = f'https://accept.paymob.com/api/acceptance/iframes/698300?payment_token={payment_key}'
        return HttpResponseRedirect(iframe_page)

    order = models.Order.objects.get(pk=merchant_order_id)
    session = order.item
    session.delete()

    result = 'Payment Failed .. '
    if payment_key == 'duplicate':
        result += "Duplicate Product ID"
    return render(
        request=request,
        template_name='order/result.html',
        context={'result': result, 'status': status}
    )


@csrf_exempt
def post_pay(request):

    hmac_secret = settings.PAYMOB_HMAC
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
        generated_hmac = hmac.new(hmac_secret.encode(
            'utf-8'), concatenated_str.encode('utf8'), hashlib.sha512).hexdigest()
        result = hmac.compare_digest(generated_hmac, sent_hmac)

        # create new zoom session
        # send session url to client

        return render(
            request=request,
            template_name='order/result.html',
            context={'result': result, 'status': True}
        )
    return HttpResponse(f'<h6>RESULT: {result}</h6>')
