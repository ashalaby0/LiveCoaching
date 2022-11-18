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
        views.BookingDetailView.as_view(),
        name='booking'
    ),
    path(
        'sessions',
        views.sessions,
        name='sessions'
    )
]
