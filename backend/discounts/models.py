from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone
from decimal import Decimal


class Discount(models.Model):
    DISCOUNT_TYPE_CHOICES = [
        ('PERCENTAGE', 'Giảm theo phần trăm'),
        ('FIXED_AMOUNT', 'Giảm số tiền cố định'),
    ]

    code = models.CharField(max_length=50, unique=True, verbose_name='Mã giảm giá',
                            help_text="Mã khách hàng sẽ nhập, ví dụ: 'SALE50', 'GIAM100K'")
    discount_type = models.CharField(max_length=20, choices=DISCOUNT_TYPE_CHOICES, verbose_name='Loại giảm giá')
    value = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal(
        '0.00'))], verbose_name='Giá trị', help_text="Nếu là phần trăm, nhập 50 cho 50%. Nếu là số tiền, nhập 100000 cho 100,000đ.")

    max_usage = models.PositiveIntegerField(
        null=True, blank=True, verbose_name='Số lần sử dụng tối đa', help_text="Bỏ trống nếu không giới hạn.")
    usage_count = models.PositiveIntegerField(default=0, editable=False, verbose_name='Số lần đã sử dụng thành công')

    valid_from = models.DateTimeField(verbose_name='Hiệu lực từ ngày')
    valid_to = models.DateTimeField(null=True, blank=True, verbose_name='Hiệu lực đến ngày',
                                    help_text="Bỏ trống nếu không có ngày hết hạn.")
    is_active = models.BooleanField(default=True, verbose_name='Đang hoạt động')

    all_users = models.BooleanField(default=True, verbose_name='Áp dụng cho tất cả người dùng')
    allowed_users = models.TextField(
        blank=True, help_text='Nhập email hoặc SĐT, mỗi giá trị cách nhau bởi dấu phẩy, không có khoảng trắng. Ví dụ: user1@gmail.com,0912345678,user2@gmail.com', verbose_name='Người dùng được phép')

    class Meta:
        verbose_name = 'Mã giảm giá'
        verbose_name_plural = 'Mã giảm giá'
        ordering = ['-valid_from']

    def __str__(self):
        if self.discount_type == 'PERCENTAGE':
            return f"{self.code} - {self.value}%"
        return f"{self.code} - {self.value:,.0f} VNĐ"

    def is_valid(self, user_email=None, user_phone=None):
        if not self.is_active:
            return False, "Mã giảm giá không hoạt động."

        now = timezone.now()
        if self.valid_from > now:
            return False, "Mã giảm giá chưa có hiệu lực."
        if self.valid_to and self.valid_to < now:
            return False, "Mã giảm giá đã hết hạn."

        pending_usages = self.usages.filter(status='PENDING').count()
        if self.max_usage is not None and (self.usage_count + pending_usages) >= self.max_usage:
            return False, "Mã giảm giá đã hết lượt sử dụng."

        if not self.all_users:
            allowed = [u.strip() for u in self.allowed_users.split(',') if u.strip()]
            if not user_email and not user_phone:
                return False, "Cần thông tin khách hàng để áp dụng mã này."
            if user_email not in allowed and user_phone not in allowed:
                return False, "Bạn không đủ điều kiện sử dụng mã giảm giá này."

        return True, "Mã hợp lệ."


class DiscountUsage(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Đang chờ thanh toán'),
        ('COMPLETED', 'Đã hoàn thành'),
        ('CANCELLED', 'Đã hủy/Thất bại'),
    ]
    discount = models.ForeignKey(Discount, on_delete=models.CASCADE, related_name='usages')
    booking = models.OneToOneField('bookings.Booking', on_delete=models.CASCADE, related_name='discount_usage')
    used_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')

    class Meta:
        verbose_name = 'Lượt sử dụng giảm giá'
        verbose_name_plural = 'Lượt sử dụng giảm giá'
