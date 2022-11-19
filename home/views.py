import datetime

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, render
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
        Q(speciality__icontains=coach_speciality_q) &
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
            Q(coach__speciality__icontains=coach_speciality_q) &
            Q(coach__price_per_hour__gte=min_price_q) &
            Q(coach__price_per_hour__lte=max_price_q) &
            Q(group_session=True)
        )
    return render(
        request=request,
        template_name='home/sessions.html',
        context={'session_list': session_list}
    )


def booking(request, coach_id):
    coach = get_object_or_404(models.Coach, pk=coach_id)
    private_session_set = models.Session.objects.filter(
        clients__contains=request.user)
    group_session_set = models.Session.objects.filter(coach__id=coach_id)

    context = {
        'private_session_set': private_session_set,
        'group_session_set': group_session_set,
        'coach': coach
    }
    return render(
        request=request,
        template_name='home/booking.html',
        context=context
    )


class BookingDetailView(DetailView):
    model = models.Coach
    template_name = 'home/booking.html'


class CoachDetailView(DetailView):
    model = models.Coach
    template_name = 'home/coach_profile.html'
