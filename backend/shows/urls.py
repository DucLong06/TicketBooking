from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ShowViewSet, PerformanceViewSet, PosterViewSet

router = DefaultRouter()
router.register('shows', ShowViewSet, basename='show')
router.register('performances', PerformanceViewSet, basename='performance')
router.register('posters', PosterViewSet, basename='poster')

urlpatterns = [
    path('', include(router.urls)),
]
