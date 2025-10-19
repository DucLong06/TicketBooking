from .models import BookingHistory
from django.utils.html import format_html, mark_safe
from django.contrib import admin
from django.utils.html import format_html
from .models import Booking, SeatReservation, BookingHistory
from django.contrib import admin
from django.utils.safestring import mark_safe
import json


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


# backend/bookings/admin.py
# THÊM HOẶC CẬP NHẬT PHẦN NÀY


@admin.register(BookingHistory)
class BookingHistoryAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'booking_or_session',  # 🟢 THAY ĐỔI: Hiển thị booking hoặc session
        'action_badge',
        'seats_count',
        'payment_amount',
        'client_ip',
        'created_at',
        'has_error'
    ]
    list_filter = [
        'action',
        'payment_status',
        'created_at',
        ('booking', admin.EmptyFieldListFilter),  # Filter có/không booking
    ]
    search_fields = [
        'booking_code',
        'session_id',
        'client_ip',
        'error_message',
        'booking__customer_email',
        'booking__customer_phone'
    ]
    readonly_fields = [
        'booking',
        'booking_code',
        'action',
        'seats_display',
        'session_id',
        'client_ip',
        'user_agent_display',
        'payment_amount',
        'payment_status',
        'gateway_response_display',
        'error_display',
        'extra_data_display',
        'created_at',
    ]
    date_hierarchy = 'created_at'

    # 🟢 THÊM ORDERING MẶC ĐỊNH: Session ID + Created At
    ordering = ['-session_id', '-created_at']

    fieldsets = (
        ('Thông tin cơ bản', {
            'fields': (
                'booking',
                'booking_code',
                'action',
                'created_at',
            )
        }),
        ('Ghế đã chọn', {
            'fields': ('seats_display',),
        }),
        ('Session & Client', {
            'fields': (
                'session_id',
                'client_ip',
                'user_agent_display',
            )
        }),
        ('Payment Info', {
            'fields': (
                'payment_amount',
                'payment_status',
                'gateway_response_display',
            )
        }),
        ('Error Info', {
            'fields': ('error_display',),
            'classes': ('collapse',),
        }),
        ('Extra Data', {
            'fields': ('extra_data_display',),
            'classes': ('collapse',),
        }),
    )

    def booking_or_session(self, obj):
        """Hiển thị booking code nếu có, nếu không thì session_id"""
        if obj.booking:
            from django.urls import reverse
            link = reverse("admin:bookings_booking_change", args=[obj.booking.id])
            return format_html(
                '<a href="{}" style="font-weight: bold; color: #0066cc;">📋 {}</a>',
                link,
                obj.booking_code
            )
        elif obj.booking_code and obj.booking_code != 'N/A':
            return format_html(
                '<span style="color: #666;">📋 {}</span>',
                obj.booking_code
            )
        else:
            session_short = obj.session_id[:8] + '...' if len(obj.session_id) > 8 else obj.session_id
            return format_html(
                '<span style="color: #999; font-family: monospace;">🔑 {}</span>',
                session_short
            )

    booking_or_session.short_description = 'Booking / Session'
    booking_or_session.admin_order_field = 'booking_code'

    def action_badge(self, obj):
        color_map = {
            'reserve_seat': '#2196F3',
            'create_booking': '#4CAF50',
            'payment_initiated': '#FF9800',
            'payment_success': '#4CAF50',
            'payment_failed': '#F44336',
            'booking_expired': '#9E9E9E',
            'booking_cancelled': '#FF5722',
            'seat_released': '#607D8B',
        }
        color = color_map.get(obj.action, '#000')
        return format_html(
            '<span style="background: {}; color: white; padding: 3px 8px; border-radius: 3px; font-size: 11px; white-space: nowrap;">{}</span>',
            color,
            obj.get_action_display()
        )
    action_badge.short_description = 'Action'

    def seats_count(self, obj):
        count = len(obj.seats_snapshot)
        if count == 0:
            return format_html('<span style="color: #999;">-</span>')
        return format_html('<span style="font-weight: bold;">{}</span>', count)
    seats_count.short_description = 'Số ghế'

    def has_error(self, obj):
        if obj.error_message:
            return format_html('<span style="color: red; font-weight: bold;">❌ Error</span>')
        return format_html('<span style="color: green;">✅ OK</span>')
    has_error.short_description = 'Status'

    def seats_display(self, obj):
        if not obj.seats_snapshot:
            return "Không có ghế"

        html = '<table style="width: 100%; border-collapse: collapse; border: 1px solid #ddd;">'
        html += '<thead><tr style="background: #f5f5f5;"><th style="padding: 8px; border: 1px solid #ddd;">Ghế</th><th style="padding: 8px; border: 1px solid #ddd;">Hàng</th><th style="padding: 8px; border: 1px solid #ddd;">Khu vực</th><th style="padding: 8px; border: 1px solid #ddd;">Giá</th><th style="padding: 8px; border: 1px solid #ddd;">Trạng thái</th></tr></thead>'
        html += '<tbody>'

        for seat in obj.seats_snapshot:
            html += f'''
            <tr>
                <td style="padding: 8px; border: 1px solid #ddd; text-align: center; font-weight: bold;">{seat.get("number", "N/A")}</td>
                <td style="padding: 8px; border: 1px solid #ddd; text-align: center;">{seat.get("row", "N/A")}</td>
                <td style="padding: 8px; border: 1px solid #ddd;">{seat.get("section_name", "N/A")}</td>
                <td style="padding: 8px; border: 1px solid #ddd; text-align: right;">{seat.get("price", 0):,.0f} ₫</td>
                <td style="padding: 8px; border: 1px solid #ddd; text-align: center;">{seat.get("status", "N/A")}</td>
            </tr>
            '''
        html += '</tbody></table>'
        return mark_safe(html)
    seats_display.short_description = 'Chi tiết ghế'

    def user_agent_display(self, obj):
        if not obj.user_agent:
            return "N/A"
        return format_html(
            '<div style="max-width: 500px; word-wrap: break-word; font-size: 12px; color: #666;">{}</div>',
            obj.user_agent
        )
    user_agent_display.short_description = 'User Agent'

    def gateway_response_display(self, obj):
        if not obj.gateway_response:
            return "N/A"
        return format_html(
            '<pre style="background: #f5f5f5; padding: 10px; border-radius: 5px; max-height: 300px; overflow: auto; font-size: 12px;">{}</pre>',
            json.dumps(obj.gateway_response, indent=2, ensure_ascii=False)
        )
    gateway_response_display.short_description = 'Gateway Response'

    def error_display(self, obj):
        if not obj.error_message:
            return format_html('<span style="color: green;">✅ Không có lỗi</span>')

        html = f'<div style="color: #d32f2f; font-weight: bold; padding: 10px; background: #ffebee; border-left: 4px solid #d32f2f; margin-bottom: 10px;">❌ Error: {obj.error_message}</div>'

        if obj.stack_trace:
            html += f'<pre style="background: #fff3f3; padding: 10px; border: 1px solid #ffccc7; border-radius: 5px; max-height: 400px; overflow: auto; margin-top: 10px; font-size: 11px;">{obj.stack_trace}</pre>'

        return mark_safe(html)
    error_display.short_description = 'Error Details'

    def extra_data_display(self, obj):
        if not obj.extra_data:
            return "N/A"
        return format_html(
            '<pre style="background: #f5f5f5; padding: 10px; border-radius: 5px; font-size: 12px;">{}</pre>',
            json.dumps(obj.extra_data, indent=2, ensure_ascii=False)
        )
    extra_data_display.short_description = 'Extra Data'

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        return False

    actions = ['view_session_journey']

    @admin.action(description='🔍 Xem toàn bộ hành trình Session')
    def view_session_journey(self, request, queryset):
        """Hiển thị tất cả action của session_id được chọn"""
        if queryset.count() != 1:
            self.message_user(request, "Vui lòng chỉ chọn 1 record để xem journey!", level='warning')
            return

        obj = queryset.first()
        session_id = obj.session_id

        if not session_id:
            self.message_user(request, "Record này không có session_id!", level='error')
            return

        from django.shortcuts import redirect
        from django.urls import reverse
        url = reverse('admin:bookings_bookinghistory_changelist')
        return redirect(f'{url}?session_id={session_id}')
