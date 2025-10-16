from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ContactInfoViewSet

router = DefaultRouter()
router.register('contact-info', ContactInfoViewSet, basename='contact-info')

urlpatterns = [
    path('', include(router.urls)),
]
