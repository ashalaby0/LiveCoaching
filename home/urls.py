from django.contrib.auth import views as auth_views
from django.urls import path

from home import views

urlpatterns = [
    path(
        '',
        views.home,
        name='home'
    ),
    path(
        'coaches',
        views.coaches,
        name='coaches'
    ),

    path(
        "password_reset",
        auth_views.PasswordResetView.as_view(
            template_name="password/password_reset.html"),
        name="password_reset"
    ),
    path(
        'password_reset/done/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='password/password_reset_done.html'),
        name='password_reset_done'
    ),
    path(
        'reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name="password/password_reset_confirm.html"),
        name='password_reset_confirm'
    ),
    path(
        'reset/done/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='password/password_reset_complete.html'),
        name='password_reset_complete'
    ),
    path(
        'coach_details/<int:pk>',
        views.CoachDetailView.as_view(),
        name='coach_details'
    ),
    path(
        'booking/<int:pk>',
        # views.BookingDetailView.as_view(),
        views.booking,
        name='booking'
    ),
    path(
        'sessions',
        views.sessions,
        name='sessions'
    ),
    path(
        'get_coach_available_hours/<int:pk>/<str:_date>',
        views.get_coach_available_hours,
        name='get_coach_available_hours'
    ),
    path(
        "payment",
        views.payment_view,
        name='payment'

    ),
    path(
        'post_pay',
        views.post_pay,
        name='post_pay'
    ),
    path(
        'schedule_zoom_meeting',
        views.schedule_zoom_meeting,
        name='schedule_zoom_meeting'
    ),
    path(
        'zoom_callback',
        views.zoom_callback,
        name='zoom_callback'
    ),

    # admin panel
    path(
        'dashboard',
        views.dashboard,
        name='dashboard'
    ),
    path(
        'dashboard/manage_coaches', 
        views.CoachAdminListView.as_view(), 
        name='manage_coaches'
    ),
    path(
        'dashboard/manage_coaches/<int:coach_id>',
        views.coach_admin_update,
        name='manage_coach'
    ),
    path(
        'contact_us',
        views.contact_us,
        name='contact_us'
    ),

    path(
        'coach_stats',
        views.coach_stats,
        name='coach_stats'
    ),

    path(
        'client_stats',
        views.client_stats,
        name='client_stats'
    ),
    path(
        'session_stats',
        views.session_stats,
        name='session_stats'
    ),
        path(
        'sessions_per_coach',
        views.sessions_per_coach,
        name='sessions_per_coach'
    ),
        path(
        'sessions_per_client',
        views.sessions_per_client,
        name='sessions_per_client'
    ),
    path(
        'get_upcomming_sessions',
        views.get_upcomming_sessions,
        name='get_upcomming_sessions'
    )


]
