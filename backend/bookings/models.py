from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal
import string
import random
from venues.models import Seat
from shows.models import Performance
from discounts.models import Discount, DiscountUsage
from django.db import transaction


def generate_booking_code():
    """Generate unique booking code"""
    length = 8
    characters = string.ascii_uppercase + string.digits
    while True:
        code = 'BK' + ''.join(random.choice(characters) for _ in range(length - 2))
        if not Booking.objects.filter(booking_code=code).exists():
            return code


class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Chờ thanh toán'),
        ('paid', 'Đã thanh toán'),
        ('cancelled', 'Đã hủy'),
        ('expired', 'Hết hạn'),
        ('refunded', 'Đã hoàn tiền'),
    ]
    SHIPPING_TIME_CHOICES = [
        ('business_hours', 'Trong giờ hành chính'),
        ('after_hours', 'Ngoài giờ hành chính'),
    ]

    booking_code = models.CharField(
        max_length=20,
        unique=True,
        default=generate_booking_code,
        verbose_name='Mã đặt vé'
    )
    performance = models.ForeignKey(
        Performance,
        on_delete=models.PROTECT,
        related_name='bookings',
        verbose_name='Suất diễn'
    )
    shipping_fee = models.DecimalField(
        max_digits=10,
        decimal_places=0,
        default=0,
        verbose_name='Phí vận chuyển'
    )
    # Customer info
    customer_name = models.CharField(max_length=200, verbose_name='Tên khách hàng')
    customer_email = models.EmailField(verbose_name='Email')
    customer_phone = models.CharField(max_length=20, verbose_name='Số điện thoại')
    customer_id_number = models.CharField(
        max_length=20,
        blank=True,
        verbose_name='CMND/CCCD'
    )

    customer_address = models.TextField(
        blank=True,
        verbose_name='Địa chỉ nhận vé'
    )
    shipping_time = models.CharField(
        max_length=50,
        choices=SHIPPING_TIME_CHOICES,
        default='business_hours',
        verbose_name='Thời gian ship'
    )

    # Booking info
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name='Trạng thái'
    )
    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=0,
        validators=[MinValueValidator(0)],
        verbose_name='Tổng tiền'
    )
    service_fee = models.DecimalField(
        max_digits=10,
        decimal_places=0,
        default=0,
        verbose_name='Phí dịch vụ'
    )
    discount_amount = models.DecimalField(
        max_digits=10,
        decimal_places=0,
        default=0,
        verbose_name='Giảm giá'
    )
    final_amount = models.DecimalField(
        max_digits=10,
        decimal_places=0,
        validators=[MinValueValidator(0)],
        verbose_name='Thành tiền'
    )

    # Session tracking
    session_id = models.CharField(max_length=100, blank=True, verbose_name='Session ID')

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    expires_at = models.DateTimeField(verbose_name='Thời gian hết hạn')
    paid_at = models.DateTimeField(null=True, blank=True, verbose_name='Thời gian thanh toán')

    # Additional info
    notes = models.TextField(blank=True, verbose_name='Ghi chú')

    discount = models.ForeignKey(Discount, on_delete=models.SET_NULL, null=True, blank=True, related_name='bookings')

    class Meta:
        verbose_name = 'Đơn đặt vé'
        verbose_name_plural = 'Đơn đặt vé'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.booking_code} - {self.customer_name}"

    def save(self, *args, **kwargs):
        if not self.expires_at:
            from django.conf import settings
            timeout_minutes = getattr(settings, 'PAYMENT_TIMEOUT_MINUTES', 15)
            self.expires_at = timezone.now() + timedelta(minutes=timeout_minutes)
        super().save(*args, **kwargs)

    @property
    def is_expired(self):
        return timezone.now() > self.expires_at and self.status == 'pending'

    def expire_booking(self):
        """
        Expires a pending booking, releasing seats and discount usage.
        Returns True if the booking was expired, False otherwise.
        """
        if self.status != 'pending' or timezone.now() < self.expires_at:
            return False

        with transaction.atomic():
            self.status = 'expired'
            self.save()

            # Release seats
            self.seat_reservations.update(status='available', session_id='', expires_at=None)

            # Release discount usage
            try:
                usage = self.discount_usage
                if usage.status == 'PENDING':
                    usage.status = 'CANCELLED'
                    usage.save()
            except DiscountUsage.DoesNotExist:
                pass  # No discount was used

        return True


class SeatReservation(models.Model):
    STATUS_CHOICES = [
        ('available', 'Trống'),
        ('reserved', 'Đang giữ'),
        ('sold', 'Đã bán'),
        ('blocked', 'Khóa'),
    ]

    booking = models.ForeignKey(
        Booking,
        on_delete=models.CASCADE,
        related_name='seat_reservations',
        null=True,
        blank=True,
        verbose_name='Đơn đặt'
    )
    performance = models.ForeignKey(
        Performance,
        on_delete=models.CASCADE,
        related_name='seat_reservations',
        verbose_name='Suất diễn'
    )
    seat = models.ForeignKey(
        Seat,
        on_delete=models.CASCADE,
        related_name='reservations',
        verbose_name='Ghế'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='available',
        verbose_name='Trạng thái'
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=0,
        validators=[MinValueValidator(0)],
        verbose_name='Giá vé'
    )

    # Session tracking for temporary reservation
    session_id = models.CharField(max_length=100, blank=True, verbose_name='Session ID')
    reserved_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True, verbose_name='Hết hạn giữ chỗ')

    client_ip = models.GenericIPAddressField(null=True, blank=True)

    class Meta:
        verbose_name = 'Ghế đặt'
        verbose_name_plural = 'Ghế đặt'
        unique_together = ['performance', 'seat']

        indexes = [
            models.Index(fields=['performance', 'seat', 'status']),
            models.Index(fields=['session_id', 'status', 'expires_at']),
            models.Index(fields=['booking', 'status']),
        ]

    def __str__(self):
        return f"{self.performance} - {self.seat} - {self.status}"

    @property
    def is_expired(self):
        if self.expires_at and self.status == 'reserved':
            return timezone.now() > self.expires_at
        return False

    def check_and_release_expired(self):
        """Release seat if reservation expired"""
        if self.is_expired:
            self.status = 'available'
            self.session_id = ''
            self.expires_at = None
            self.save()
            return True
        return False


class BookingHistory(models.Model):
    ACTION_CHOICES = [
        ('reserve_seat', 'Đặt giữ chỗ'),
        ('create_booking', 'Tạo booking'),
        ('payment_initiated', 'Bắt đầu thanh toán'),
        ('payment_success', 'Thanh toán thành công'),
        ('payment_failed', 'Thanh toán thất bại'),
        ('booking_expired', 'Booking hết hạn'),
        ('booking_cancelled', 'Hủy booking'),
        ('seat_released', 'Giải phóng ghế'),
    ]

    booking = models.ForeignKey(
        'Booking',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='history'
    )
    booking_code = models.CharField(max_length=10, db_index=True)
    action = models.CharField(max_length=50, choices=ACTION_CHOICES)

    seats_snapshot = models.JSONField(
        default=list,
        help_text="Danh sách ghế tại thời điểm action xảy ra"
    )

    # Metadata
    session_id = models.CharField(max_length=255, blank=True)
    client_ip = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)

    payment_amount = models.DecimalField(
        max_digits=10,
        decimal_places=0,
        null=True,
        blank=True
    )
    payment_status = models.CharField(max_length=50, blank=True)
    gateway_response = models.JSONField(default=dict, blank=True)

    # Error info
    error_message = models.TextField(blank=True)
    stack_trace = models.TextField(blank=True)

    # Extra data
    extra_data = models.JSONField(default=dict, blank=True)

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['booking_code', '-created_at']),
            models.Index(fields=['session_id', '-created_at']),
        ]
        verbose_name = 'Booking History'
        verbose_name_plural = 'Booking Histories'

    def __str__(self):
        return f"{self.booking_code} - {self.get_action_display()} - {self.created_at}"

    @staticmethod
    def log_action(booking, action, request=None, seats=None, error=None, **kwargs):
        """
        Helper method để log action

        Usage:
        BookingHistory.log_action(
            booking=booking,
            action='payment_failed',
            request=request,
            seats=seat_reservations,
            error=str(e),
            gateway_response=response_data
        )
        """
        seats_data = []
        if seats:
            for seat in seats:
                if hasattr(seat, 'seat'):
                    seats_data.append({
                        'seat_id': seat.seat.id,
                        'row': seat.seat.row.label,
                        'number': seat.seat.display_label,
                        'price': float(seat.price),
                        'status': seat.status,
                    })

        client_ip = None
        user_agent = ''
        if request:
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                client_ip = x_forwarded_for.split(',')[0].strip()
            else:
                client_ip = request.META.get('REMOTE_ADDR')
            user_agent = request.META.get('HTTP_USER_AGENT', '')

        return BookingHistory.objects.create(
            booking=booking,
            booking_code=booking.booking_code if booking else kwargs.get('booking_code', 'N/A'),
            action=action,
            seats_snapshot=seats_data,
            session_id=booking.session_id if booking else kwargs.get('session_id', ''),
            client_ip=client_ip,
            user_agent=user_agent,
            payment_amount=kwargs.get('payment_amount'),
            payment_status=kwargs.get('payment_status', ''),
            gateway_response=kwargs.get('gateway_response', {}),
            error_message=error or '',
            stack_trace=kwargs.get('stack_trace', ''),
            extra_data=kwargs.get('extra_data', {}),
        )
