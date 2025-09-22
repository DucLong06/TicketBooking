from django.urls import path
from .views import (
    create_payment,
    vnpay_return,
    check_payment_status
)

urlpatterns = [
    path('bookings/<str:booking_code>/payment/', create_payment, name='create_payment'),
    path('payment/<str:transaction_id>/status/', check_payment_status, name='check_payment_status'),
    path('payment/vnpay/return/', vnpay_return, name='vnpay_return'),  # ✅ Thêm dòng này
]
