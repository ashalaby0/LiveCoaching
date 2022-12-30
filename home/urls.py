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
        'zoom_schedule_callback',
        views.zoom_schedule_callback,
        name='zoom_schedule_callback'
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
        'sessions_per_category',
        views.sessions_per_category,
        name='sessions_per_category'
    ),
    
  
    path(
        'tst_usr_zoom_meetings',
        views.got_to_zoom_meeting_join_page,
        name='tst_usr_zoom_meetings'
    ),
    path(
        'tst_open_zoom_meeting',
        views.open_zoom_meeting,
        name='tst_open_zoom_meeting'
    ),
    # url to get zoom sdk credentials
    path(
        'EmbdZmCrd',
        views.get_zoom_crd_creds,
        name='EmbdZmCrd'
    ),
    path(
        'get_sorted_coaches/<str:option>/<str:coach_name_q>/<str:coach_speciality_q>/<str:min_price_q>/<str:max_price_q>',
        views.get_sorted_coaches,
        name='get_sorted_coaches'
    ),
    path(
        'signup',
        views.signup_view,
        name='signup'
    ),

    path(
        'customer_messages',
        views.customer_messages,
        name='customer_messages'
    ),
    path(
        'close_customer_message',
        views.close_customer_message,
        name='close_customer_message'
    ),
    path(
        'promo_codes',
        views.promo_codes,
        name='promo_codes'
    ),
    path(
        'end_promo_code',
        views.end_promo_code,
        name='end_promo_code'
    ),
    path(
        'generate_new_promo_code',
        views.generate_new_promo_code,
        name='generate_new_promo_code'
    ),
    path(
        'validate_promo_code',
        views.validate_promo_code,
        name='validate_promo_code'
    )



]
