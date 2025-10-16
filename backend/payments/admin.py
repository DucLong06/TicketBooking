from django.contrib import admin, messages
from django.utils.html import format_html
from django.urls import reverse
from .models import Payment
from payments.ninepay import NinePay
from bookings.tasks import update_payment_success, update_payment_failed


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        'transaction_id',
        'booking_link',
        'amount_formatted',
        'status_colored',
        'payment_method',
        'created_at'
    )
    list_filter = ('status', 'payment_method', 'created_at')
    search_fields = ('transaction_id', 'booking__booking_code', 'gateway_transaction_id')
    readonly_fields = ('booking', 'created_at', 'updated_at', 'paid_at', 'gateway_response', 'gateway_transaction_id')
    list_per_page = 25
    actions = ['check_9pay_status', 'mark_as_successful_manual']

    def booking_link(self, obj):
        link = reverse("admin:bookings_booking_change", args=[obj.booking.id])
        return format_html('<a href="{}">{}</a>', link, obj.booking.booking_code)
    booking_link.short_description = 'Mã Booking'
    booking_link.admin_order_field = 'booking__booking_code'

    def amount_formatted(self, obj):
        return f"{obj.amount:,.0f} VNĐ"
    amount_formatted.short_description = 'Số tiền'
    amount_formatted.admin_order_field = 'amount'

    def status_colored(self, obj):
        colors = {
            'pending': 'orange',
            'success': 'green',
            'failed': 'red',
            'cancelled': 'gray',
        }
        color = colors.get(obj.status, 'black')
        return format_html('<span style="color: {}; font-weight: bold;">{}</span>', color, obj.get_status_display())
    status_colored.short_description = 'Trạng thái'
    status_colored.admin_order_field = 'status'

    @admin.action(description='Kiểm tra lại trạng thái với 9Pay')
    def check_9pay_status(self, request, queryset):
        pending_payments = queryset.filter(status='pending')

        if not pending_payments.exists():
            self.message_user(request, "Chỉ có thể kiểm tra các giao dịch đang 'Chờ xử lý'.", messages.WARNING)
            return

        ninepay = NinePay()
        success_count = 0
        failed_count = 0
        error_count = 0

        for payment in pending_payments:
            result = ninepay.query_payment_status(payment.transaction_id)
            if not result['success']:
                error_count += 1
                continue

            status_code = result['status']
            error_code = result['error_code']
            data = result['data']

            if status_code == 5 and error_code == '000':
                if update_payment_success(payment, data):
                    success_count += 1
            elif status_code in [6, 8, 9]:  # Failed, Cancelled, Rejected
                if update_payment_failed(payment, data):
                    failed_count += 1

        self.message_user(
            request, f"Kiểm tra hoàn tất: {success_count} thành công, {failed_count} thất bại, {error_count} lỗi truy vấn.", messages.SUCCESS)

    @admin.action(description='⚠️ Đánh dấu thành công (Thủ công)')
    def mark_as_successful_manual(self, request, queryset):
        payments_to_update = queryset.filter(status__in=['pending', 'failed'])
        count = 0
        for payment in payments_to_update:
            mock_gateway_response = {
                'status': 5,
                'error_code': '000',
                'payment_no': f'MANUAL_{payment.transaction_id}',
                'message': f'Marked as successful manually by admin user: {request.user.username}'
            }
            if update_payment_success(payment, mock_gateway_response):
                count += 1

        self.message_user(request, f"Đã cập nhật thủ công {count} giao dịch thành công.", messages.SUCCESS)
