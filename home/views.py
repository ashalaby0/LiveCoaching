import datetime

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
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


# class BookingDetailView(DetailView):
#     model = models.Coach
#     template_name = 'home/booking.html'


class CoachDetailView(DetailView):
    model = models.Coach
    template_name = 'home/coach_profile.html'


def payment_view(request):

    print('post', request.POST)
    coach_id = request.POST.get('coach_id')
    session_hour = request.POST.get('sessionHour')
    session_hour = int(session_hour.split(':')[0])
    session_date = request.POST.get('session_date')
    _year, _month, _day = session_date.split('-')
    _year = int(_year)
    _month = int(_month)
    _day = int(_day)

    client = models.Client.objects.get(user=request.user)
    print(client)
    _time = datetime.datetime(
        _year, _month, _day, session_hour, 0, 0)
    coach = models.Coach.objects.get(pk=coach_id)
    new_session = models.Session.objects.create(
        coach=coach, time=_time, category=coach.speciality, group_session=False)
    new_session.clients.add(client)

    print(f'session created: {new_session.id}')

    new_order = models.Order.objects.create(client=client, item=new_session)

    print(f'order created: {new_order.id}')

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
        generated_hmac = hmac.new(hmac_secret.encode(
            'utf-8'), concatenated_str.encode('utf8'), hashlib.sha512).hexdigest()
        result = hmac.compare_digest(generated_hmac, sent_hmac)

        return render(
            request=request,
            template_name='order/result.html',
            context={'result': result, 'status': True}
        )
    return HttpResponse(f'<h6>RESULT: {result}</h6>')
