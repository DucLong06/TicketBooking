from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone
from datetime import timedelta
import string
import random
from venues.models import Seat
from shows.models import Performance

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
    
    # Customer info
    customer_name = models.CharField(max_length=200, verbose_name='Tên khách hàng')
    customer_email = models.EmailField(verbose_name='Email')
    customer_phone = models.CharField(max_length=20, verbose_name='Số điện thoại')
    customer_id_number = models.CharField(
        max_length=20, 
        blank=True,
        verbose_name='CMND/CCCD'
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
    
    class Meta:
        verbose_name = 'Đơn đặt vé'
        verbose_name_plural = 'Đơn đặt vé'
        ordering = ['-created_at']
        
    def __str__(self):
        return f"{self.booking_code} - {self.customer_name}"
    
    def save(self, *args, **kwargs):
        if not self.expires_at:
            from django.conf import settings
            timeout_minutes = getattr(settings, 'BOOKING_TIMEOUT_MINUTES', 10)
            self.expires_at = timezone.now() + timedelta(minutes=timeout_minutes)
        super().save(*args, **kwargs)
    
    @property
    def is_expired(self):
        return timezone.now() > self.expires_at and self.status == 'pending'
    
    def check_and_update_expiry(self):
        """Check if booking is expired and update status"""
        if self.is_expired:
            self.status = 'expired'
            self.save()
            # Release seats
            self.seat_reservations.update(status='available')
            return True
        return False


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
    
    class Meta:
        verbose_name = 'Ghế đặt'
        verbose_name_plural = 'Ghế đặt'
        unique_together = ['performance', 'seat']
        
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