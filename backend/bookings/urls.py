from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    BookingViewSet,
    performance_seat_map,
    reserve_seats,
    release_seats
)

router = DefaultRouter()
router.register('bookings', BookingViewSet, basename='booking')

urlpatterns = [
    path('', include(router.urls)),
    path('performances/<int:performance_id>/seat-map/', performance_seat_map, name='seat-map'),
    path('seats/reserve/', reserve_seats, name='reserve-seats'),
    path('seats/release/', release_seats, name='release-seats'),
]
