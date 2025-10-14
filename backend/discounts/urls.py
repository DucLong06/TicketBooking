from django.urls import path
from .views import apply_discount

urlpatterns = [
    path('discounts/apply/', apply_discount, name='apply-discount'),
]
