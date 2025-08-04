from django.db import models
from django.core.validators import MinValueValidator
from bookings.models import Booking


class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('vnpay', 'VNPay'),
        ('momo', 'MoMo'),
        ('bank', 'Chuyển khoản'),
        ('card', 'Thẻ quốc tế'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Chờ xử lý'),
        ('processing', 'Đang xử lý'),
        ('success', 'Thành công'),
        ('failed', 'Thất bại'),
        ('cancelled', 'Đã hủy'),
        ('refunded', 'Đã hoàn tiền'),
    ]

    booking = models.ForeignKey(
        Booking,
        on_delete=models.CASCADE,
        related_name='payments',
        verbose_name='Đơn đặt vé'
    )
    transaction_id = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='Mã giao dịch'
    )
    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHOD_CHOICES,
        verbose_name='Phương thức thanh toán'
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=0,
        validators=[MinValueValidator(0)],
        verbose_name='Số tiền'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name='Trạng thái'
    )

    # Payment gateway response
    gateway_response = models.JSONField(
        default=dict,
        blank=True,
        verbose_name='Response từ gateway'
    )
    gateway_transaction_id = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='Mã GD từ gateway'
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    paid_at = models.DateTimeField(null=True, blank=True, verbose_name='Thời gian thanh toán')

    # Additional info
    notes = models.TextField(blank=True, verbose_name='Ghi chú')

    class Meta:
        verbose_name = 'Thanh toán'
        verbose_name_plural = 'Thanh toán'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.transaction_id} - {self.amount:,.0f}đ - {self.status}"
