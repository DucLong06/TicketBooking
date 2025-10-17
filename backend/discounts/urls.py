from django.urls import path
from .views import get_available_discounts, validate_discount_code

urlpatterns = [
    path('discounts/available/', get_available_discounts, name='available-discounts'),
    path('discounts/validate/', validate_discount_code, name='validate-discount'),
]
