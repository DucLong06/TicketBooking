from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.contrib.admin.views.decorators import staff_member_required
from markdownx.views import MarkdownifyView, ImageUploadView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('shows.urls')),
    path('api/', include('bookings.urls')),
    path('api/', include('payments.urls')),
    path('api/', include('venues.urls')),

    path('markdownx/upload/',
         staff_member_required(ImageUploadView.as_view()),
         name='markdownx_upload'),
    path('markdownx/markdownify/',
         staff_member_required(MarkdownifyView.as_view()),
         name='markdownx_markdownify'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += [
    re_path(r'^.*$', TemplateView.as_view(template_name='index.html')),
]
