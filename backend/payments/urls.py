from django.urls import path
from .views import (
    create_payment,
    check_payment_status,
    ninepay_return
)

urlpatterns = [
    path('bookings/<str:booking_code>/payment/', create_payment, name='create_payment'),
    path('payment/<str:transaction_id>/status/', check_payment_status, name='check_payment_status'),
    # path('payment/vnpay/return/', vnpay_return, name='vnpay_return'),
    path('payment/ninepay/return/', ninepay_return, name='ninepay_return'),
]
