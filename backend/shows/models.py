from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone
from venues.models import Venue, PriceCategory
from markdownx.models import MarkdownxField


class Show(models.Model):
    name = models.CharField(max_length=200, verbose_name='Tên vở diễn')
    slug = models.SlugField(max_length=200, unique=True, verbose_name='Slug')
    category = models.CharField(max_length=100, verbose_name='Thể loại')
    duration_minutes = models.IntegerField(
        validators=[MinValueValidator(1)],
        verbose_name='Thời lượng (phút)'
    )
    description = models.TextField(verbose_name='Mô tả')
    poster = models.ImageField(
        upload_to='shows/posters/',
        blank=True,
        null=True,
        verbose_name='Poster'
    )
    trailer_url = models.URLField(
        blank=True,
        null=True,
        verbose_name='Link YouTube Trailer',
        help_text='Link YouTube trailer (vd: https://www.youtube.com/watch?v=xxxxx)'
    )

    description_markdown = MarkdownxField(
        blank=True,
        verbose_name='Mô tả chi tiết (Markdown)',
        help_text='Sử dụng Markdown để định dạng văn bản. Hỗ trợ: **bold**, *italic*, [links](url), ![images](url), ### headings, etc.'
    )

    venue = models.ForeignKey(Venue, on_delete=models.CASCADE, verbose_name='Nhà hát')
    is_active = models.BooleanField(default=True, verbose_name='Đang hoạt động')

    service_fee_per_ticket = models.DecimalField(
        max_digits=10,
        decimal_places=0,
        default=10000,
        validators=[MinValueValidator(0)],
        verbose_name='Phí dịch vụ mỗi vé',
        help_text='Phí dịch vụ tính cho mỗi vé (VNĐ)'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Vở diễn'
        verbose_name_plural = 'Vở diễn'
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class Performance(models.Model):
    STATUS_CHOICES = [
        ('scheduled', 'Đã lên lịch'),
        ('on_sale', 'Đang bán'),
        ('sold_out', 'Hết vé'),
        ('cancelled', 'Đã hủy'),
        ('completed', 'Đã diễn'),
    ]

    show = models.ForeignKey(Show, on_delete=models.CASCADE, related_name='performances')
    datetime = models.DateTimeField(verbose_name='Ngày giờ diễn')
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='scheduled',
        verbose_name='Trạng thái'
    )
    notes = models.TextField(blank=True, verbose_name='Ghi chú')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    shipping_fee = models.DecimalField(
        max_digits=10,
        decimal_places=0,
        default=0,
        verbose_name='Phí vận chuyển'
    )

    max_tickets_per_booking = models.PositiveIntegerField(
        default=8,
        verbose_name='Số vé tối đa mỗi đơn',
        help_text='Số lượng vé tối đa khách hàng có thể đặt trong suất diễn này'
    )

    class Meta:
        verbose_name = 'Suất diễn'
        verbose_name_plural = 'Suất diễn'
        ordering = ['datetime']

    def __str__(self):
        return f"{self.show.name} - {self.datetime.strftime('%d/%m/%Y %H:%M')}"

    @property
    def is_past(self):
        return self.datetime < timezone.now()

    @property
    def available_seats_count(self):
        from bookings.models import SeatReservation
        total_seats = self.show.venue.sections.aggregate(
            total=models.Count('rows__seats')
        )['total'] or 0

        reserved_seats = SeatReservation.objects.filter(
            performance=self,
            status__in=['reserved', 'sold']
        ).count()

        return total_seats - reserved_seats


class PerformancePrice(models.Model):
    performance = models.ForeignKey(
        Performance,
        on_delete=models.CASCADE,
        related_name='prices'
    )
    price_category = models.ForeignKey(
        PriceCategory,
        on_delete=models.CASCADE
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=0,
        validators=[MinValueValidator(0)],
        verbose_name='Giá'
    )

    class Meta:
        verbose_name = 'Giá suất diễn'
        verbose_name_plural = 'Giá suất diễn'
        unique_together = ['performance', 'price_category']

    def __str__(self):
        return f"{self.performance} - {self.price_category.name}: {self.price:,.0f}đ"


class Poster(models.Model):
    """Banner/Poster slides for homepage"""
    title = models.CharField(max_length=200, verbose_name='Tiêu đề')
    image = models.ImageField(
        upload_to='posters/',
        verbose_name='Ảnh poster',
        help_text='Kích thước khuyến nghị: 1920x600px cho desktop, tự động resize cho mobile'
    )
    show = models.ForeignKey(
        Show,
        on_delete=models.CASCADE,
        related_name='posters',
        verbose_name='Vở diễn liên kết'
    )
    order = models.IntegerField(
        default=0,
        verbose_name='Thứ tự hiển thị',
        help_text='Số nhỏ hơn sẽ hiển thị trước'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Đang hoạt động'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Banner/Poster'
        verbose_name_plural = 'Banner/Poster'
        ordering = ['order', '-created_at']

    def __str__(self):
        return f"{self.title} - {self.show.name}"
