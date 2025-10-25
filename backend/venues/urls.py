from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ContactInfoViewSet
from venues.views import toggle_row_orphan_rule, toggle_venue_orphan_rule


router = DefaultRouter()
router.register('contact-info', ContactInfoViewSet, basename='contact-info')

urlpatterns = [
    path('', include(router.urls)),
    path('api/rows/<int:row_id>/toggle-orphan-rule/',
         toggle_row_orphan_rule,
         name='toggle_row_orphan_rule'),
    path('api/venues/<int:venue_id>/toggle-orphan-rule/',
         toggle_venue_orphan_rule,
         name='toggle_venue_orphan_rule'),
]
