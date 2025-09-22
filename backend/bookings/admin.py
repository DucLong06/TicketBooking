from django.contrib import admin
from django.utils.html import format_html
from .models import Booking, SeatReservation


class SeatReservationInline(admin.TabularInline):
    model = SeatReservation
    extra = 0
    readonly_fields = ['seat', 'price', 'status']
    can_delete = False


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = [
        'booking_code',
        'customer_name',
        'performance',
        'status_colored',
        'final_amount',
        'created_at'
    ]
    list_filter = ['status', 'performance__show', 'created_at']
    search_fields = ['booking_code', 'customer_name', 'customer_email', 'customer_phone']
    readonly_fields = [
        'booking_code',
        'created_at',
        'updated_at',
        'expires_at',
        'paid_at'
    ]
    inlines = [SeatReservationInline]
    date_hierarchy = 'created_at'

    def status_colored(self, obj):
        colors = {
            'pending': 'orange',
            'paid': 'green',
            'cancelled': 'red',
            'expired': 'gray',
            'refunded': 'blue',
        }
        color = colors.get(obj.status, 'black')
        return format_html(
            '<span style="color: {};">{}</span>',
            color,
            obj.get_status_display()
        )
    status_colored.short_description = 'Trạng thái'

    actions = ['mark_as_paid', 'mark_as_cancelled']

    def mark_as_paid(self, request, queryset):
        queryset.update(status='paid')
        self.message_user(request, f"{queryset.count()} đơn đã được đánh dấu là đã thanh toán.")
    mark_as_paid.short_description = "Đánh dấu đã thanh toán"

    def mark_as_cancelled(self, request, queryset):
        queryset.update(status='cancelled')
        # Release seats
        for booking in queryset:
            booking.seat_reservations.update(status='available')
        self.message_user(request, f"{queryset.count()} đơn đã được hủy.")
    mark_as_cancelled.short_description = "Hủy đơn đặt vé"


@admin.register(SeatReservation)
class SeatReservationAdmin(admin.ModelAdmin):
    list_display = ['performance', 'seat', 'status', 'booking', 'price', 'reserved_at']
    list_filter = ['status', 'performance__show', 'performance']
    search_fields = ['seat__row__label', 'seat__number', 'booking__booking_code']
    list_editable = ['status']
    date_hierarchy = 'reserved_at'

    actions = ['release_seats']

    def release_seats(self, request, queryset):
        queryset.update(status='available', session_id='', expires_at=None)
        self.message_user(request, f"{queryset.count()} ghế đã được giải phóng.")
    release_seats.short_description = "Giải phóng ghế"
