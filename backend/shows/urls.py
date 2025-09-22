from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ShowViewSet, PerformanceViewSet

router = DefaultRouter()
router.register('shows', ShowViewSet, basename='show')
router.register('performances', PerformanceViewSet, basename='performance')

urlpatterns = [
    path('', include(router.urls)),
]
