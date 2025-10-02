from django.contrib import admin
from django.db.models import Count, Sum
from django.utils.html import format_html
from shows.models import Show, Performance
from bookings.models import Booking
from payments.models import Payment


class DashboardAdmin(admin.AdminSite):
    site_header = "Theater Booking Dashboard"

    def index(self, request, extra_context=None):
        extra_context = extra_context or {}

        extra_context['total_shows'] = Show.objects.filter(is_active=True).count()
        extra_context['total_performances'] = Performance.objects.filter(
            status='on_sale'
        ).count()
        extra_context['total_bookings'] = Booking.objects.filter(
            status='confirmed'
        ).count()

        total_revenue = Payment.objects.filter(
            status='completed'
        ).aggregate(Sum('amount'))['amount__sum'] or 0
        extra_context['total_revenue'] = total_revenue

        return super().index(request, extra_context)


admin.site = DashboardAdmin(name='admin')
