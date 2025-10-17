from django.urls import path
from . import views

urlpatterns = [
    path('discounts/available/', views.get_available_discounts, name='available-discounts'),
]
