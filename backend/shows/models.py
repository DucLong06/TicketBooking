from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone
from venues.models import Venue, PriceCategory


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
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE, verbose_name='Nhà hát')
    is_active = models.BooleanField(default=True, verbose_name='Đang hoạt động')
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
