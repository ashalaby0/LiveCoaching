import base64
import datetime
import hashlib
import hmac

import requests
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail, EmailMessage
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView
from django.core import serializers


from . import forms, models, serializers


def home(request):
    return render(
        request=request,
        template_name='home/home.html',
        context={}
    )


# @login_required(login_url='/accounts/login')
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


# @login_required(login_url='/accounts/login')
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


def get_coach_available_hours(request, pk, _date):
    hours = models.Coach.objects.get_available_hours(pk, _date)
    return JsonResponse({'av_hours': hours})


def booking(request, pk):
    client, status = models.Client.objects.get_or_create(user=request.user)
    print(client)

    coach = get_object_or_404(models.Coach, pk=pk)
    private_session_set = models.Session.objects.filter(clients=client.id).filter(coach__id=pk).filter(group_session=False)
    group_session_set = models.Session.objects.filter(coach__id=pk).filter(coach__id=pk).filter(group_session=True)

    context = {
        'private_session_set': private_session_set,
        'group_session_set': group_session_set,
        'coach': coach,
        'session_form': forms.SessionModelForm(),
        'today': datetime.datetime.now().strftime('%Y-%m-%d')
    }
    return render(
        request=request,
        template_name='home/booking.html',
        context=context
    )


class CoachDetailView(DetailView):
    model = models.Coach
    template_name = 'home/coach_profile.html'

def _get_zoom_token(request):
    ZOOM_OAUTH_REDIRECT_URL = request.build_absolute_uri(
        reverse(settings.ZOOM_OAUTH_REDIRECT_URL_NAME))
    return redirect(settings.ZOOM_USER_AUTHORIZATON_URL_BASE + ZOOM_OAUTH_REDIRECT_URL)

def schedule_zoom_meeting(request):
    return _get_zoom_token(request)
    

def zoom_schedule_callback(request):
    response = requests.post(
        url=settings.ZOOM_TOKEN_REQUEST_URL,
        headers={
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': 'Basic ' + base64.b64encode(bytes(f'{settings.ZOOM_API_KEY}:{settings.ZOOM_API_SEC}', 'utf-8')).decode('utf-8')
        },
        data={
            'code': request.GET.get('code'),
            'grant_type': 'authorization_code',
            'redirect_uri': request.build_absolute_uri(reverse('zoom_schedule_callback'))
        }
    )
    access_token = response.json()['access_token']
    meeting_date = request.session['meeting_date']
    meeting_topic = request.session['meeting_topic']
    meeting_agenda = request.session['meeting_agenda']
    client_mail = request.session['client_mail']
    coach_mail = request.session['coach_mail']
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
            'schedule_for': settings.EMAIL_HOST_USER,
            'schedule_time': meeting_date,
            'timezone': 'Egypt/Cairo',
            'Topic': meeting_topic,
            'type': 2
        }
    )
    
    print(response.json())
    start_url = response.json()['start_url']
    send_mail(
        'LifeCoaching Session Scheduled',
        f'URL:{start_url} <br> CLIENT: {request.user.username}',
        settings.EMAIL_HOST_USER,
        [client_mail, coach_mail],
        fail_silently=False,
    )

    join_url = response.json()['join_url']
    send_mail(
        'LifeCoaching Session Scheduled',
        f'URL:{join_url}',
        settings.EMAIL_HOST_USER,
        [client_mail, coach_mail],
        fail_silently=False,
    )

    messages.success(request, f"Session Scheduled Successfully & Link sent by mail. {request.user.email}")
    return redirect('home')

def zoom_meeting_callback(request):
    # not done yet
    return redirect('home')

def payment_view(request):

    coach_id = request.POST.get('coach_id')
    session_hour = request.POST.get('sessionHour')
    session_hour, session_minute = [int(x) for x in session_hour.split(':')]
    session_date = request.POST.get('session_date')
    _year, _month, _day = session_date.split('-')
    _year = int(_year)
    _month = int(_month)
    _day = int(_day)

    meeting_date = datetime.datetime(
        _year, _month, _day, session_hour, session_minute).strftime('%Y-%m-%d%T%H:%M')
    meeting_topic = ''
    meeting_agenda = ''

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
        merchant_order_id=merchant_order_id,
        coach=coach,
        client=client
    )

    request.session['meeting_date'] = meeting_date
    request.session['meeting_topic'] = meeting_topic
    request.session['meeting_agenda'] = meeting_agenda
    request.session['client_mail'] = client.user.email
    request.session['coach_mail'] = coach.user.email
    print(f'client_mail: {client.user.email}')

    if status:
        iframe_page = f'https://accept.paymob.com/api/acceptance/iframes/698300?payment_token={payment_key}'
        return HttpResponseRedirect(iframe_page)

    order = models.Order.objects.get(pk=merchant_order_id)
    session = order.item
    session.delete()

    result = 'Payment Failed .. '
    if payment_key == 'duplicate':
        result += "Duplicate Product ID"

    else:
        result += str(payment_key)
    return render(
        request=request,
        template_name='order/result.html',
        context={'result': result, 'status': status}
    )


@ csrf_exempt
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

        error_occured = request.GET.get('error_occured')
        error_message = request.GET.get('error.message')
        message = f'Failed with Error Message: {error_message}'
        if error_occured == 'true':
            return render(
            request=request,
            template_name='order/result.html',
            context={'result': message, 'status': True}
        )
        
            
        sent_hmac = request.GET.get('hmac')
        concatenated_str = ''.join(request.GET.get(i) for i in hmac_fields)
        generated_hmac = hmac.new(hmac_secret.encode(
            'utf-8'), concatenated_str.encode('utf8'), hashlib.sha512).hexdigest()
        result = hmac.compare_digest(generated_hmac, sent_hmac)
        
        print(f'hmac varification result: {result}')
        print(f'payment success: {request.GET.get("success")}')
        if request.GET.get("success") == 'true':
            return redirect('schedule_zoom_meeting')

    
    messages.error(request, f"Payment failed, insure your credit card inputs are correct and try again.")
    return redirect('home')
    #     return render(
    #         request=request,
    #         template_name='order/result.html',
    #         context={'result': request.GET.get("success"), 'status': True}
    #     )
    # return HttpResponse(f'<h6>RESULT: {result}</h6>')


# admin panel

def dashboard(request):
    upcomming_sessions = models.Session.objects.get_upcomming_sessions()
    new_customer_messages = models.CustomerMessage.objects.all()



    context = {
        'upcomming_sessions':upcomming_sessions,
        'new_customer_messages': new_customer_messages
    }
    return render(request, template_name="home/dashboard.html", context=context)


class CoachAdminListView(ListView):
    model = models.Coach
    template_name = 'home/manage_coaches.html'


def coach_admin_update(request, coach_id):

    coach = models.Coach.objects.get(pk=coach_id)
    user = coach.user

    if request.method == 'POST':

        coach_form = forms.CoachModelForm(request.POST, instance=coach)
        user_form = forms.UserModelForm(request.POST, instance=user)
        if coach_form.is_valid() and user_form.is_valid():
            coach_form.save()
            user_form.save()
            return redirect('manage_coaches')
    else:
        user_form = forms.UserModelForm(instance=user)
        coach_form = forms.CoachModelForm(instance=coach)


    return render(
        request=request,
        template_name='home/manage_coach.html',
        context={
            'user_form': user_form,
            'coach_form': coach_form
        }
    )

def contact_us(request):

    form = forms.CustomerMessageForm()
    context = {'form': form}

    if request.method == 'POST':
        form = forms.CustomerMessageForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Submitted Successfully !.")
            form = forms.CustomerMessageForm()
            context = {'form': form}


        subject = 'New Customer Message'
        html_content = f"""
        <span><strong>Name</strong></span>:  <span>{request.POST['full_name']}</span>
        <br>
        <span><strong>Email</strong></span>: <span>{request.POST['email']}</span>
        <br>
        <span><strong>Message</strong></span>: <span>{request.POST['message']}</span>
        <br>
        """
        from_email = settings.EMAIL_HOST_USER
        to_list = [settings.EMAIL_HOST_USER]

        msg = EmailMessage(subject, html_content, from_email, to_list)
        msg.content_subtype = "html"  # Main content is now text/html
        msg.send()
        print('mail sent')


    return render(
        request=request,
        template_name='home/contact_us.html',
        context=context
    )


def coach_stats(request):
    result = models.Coach.objects.get_monthly_stats()
    return JsonResponse(
        {i['joined_at__month']: i['count'] for i in result}
    )


def client_stats(request):
    result = models.Client.objects.get_monthly_stats()
    return JsonResponse(
        {i['joined_at__month']: i['count'] for i in result}
    )


def session_stats(request):
    result = models.Session.objects.get_monthly_stats()
    return JsonResponse(
        {i['time__month']: i['count'] for i in result}
    )


def sessions_per_coach(request):
    result = models.Session.objects.get_total_session_per_coach()
    return JsonResponse(
        {i['coach__user__username']:i['count'] for i in result}
    )


def sessions_per_client(request):
    result = models.Client.objects.get_total_session_per_client()
    return JsonResponse(
        {i['user__username']:i['no_of_session'] for i in result}
        # user__username', 'no_of_sessions
    )


def get_upcomming_sessions(request):
    print(result)
    return JsonResponse(
        {'sessions': [x for x in result]}
    )

# gets upcomming user sessions zoom meetings for current user
def user_upcomming_zoom_meetings(reqeust):
    meetings = models.ZoomMeeting.objects.upcomming_meetings(request.user)
    # this page should load user home page with all upcommign meetings as buttons
    return render(
        request=request,
        template_name='home/user_home_page.html',
        context={'meetings':meetings, 'ps':settings.ZOOM_MEETING_PASSWORD}
    )
    
def got_to_zoom_meeting_join_page(request):
    # this page should load the zoom meeting joinning page with only JOIN Button and all fields are hidden
    return render(
        request=request,
        template_name='home/tst_usr_zoom_meetings.html',
        context={'nm':'72325261745', 'ps':'Gi8Ze5'} # temp for testing
        # context={'number':'72325261745', 'ps':settings.ZOOM_MEETING_PASSWORD}
    )


def open_zoom_meeting(request):
    return render(
        request,
        template_name='home/zoom/meeting.html',
        context={}
    )

def get_zoom_crd_creds(request):
    return JsonResponse(
        {'key':'VFlelbBM10XSBHmxUgUGfSsFqR3bQGdy8IkE', 'pass':'QUasaMms1KhNcqRHBRmU2KCQlFEbs2wJKHpK'}
    )

def get_sorted_coaches(request, option, coach_name_q, coach_speciality_q, min_price_q, max_price_q):
    media_url = settings.MEDIA_URL 
    sorted_coaches = models.Coach.objects.filter(price_per_hour__gte=min_price_q).filter(price_per_hour__lte=max_price_q)

    if coach_name_q.lower() != 'empty':
        sorted_coaches = sorted_coaches.filter(user__username__icontains=coach_name_q.strip())
    if coach_speciality_q.lower() != 'empty':
        sorted_coaches = sorted_coaches.filter(speciality__name__icontains=coach_name_q.strip())

    if option == 'plh':
        sorted_coaches = sorted_coaches.order_by('price_per_hour')
    elif option == 'phl':
        sorted_coaches = sorted_coaches.order_by('-price_per_hour')
    elif option == 'ctchna':
        sorted_coaches = sorted_coaches.order_by('user__username')
    elif option == 'catna':
        sorted_coaches = sorted_coaches.order_by('speciality__name')


    serialized_sorted_coaches = [serializers.CoachSerializer(instance=i).data for i in (x for x in sorted_coaches)]
    return JsonResponse(
        {'sorted_coaches':serialized_sorted_coaches}
    )