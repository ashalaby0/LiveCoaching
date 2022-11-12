from django.urls import path

from . import views

urlpatterns = [
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

]