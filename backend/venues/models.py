from django.db import models
from django.core.validators import MinValueValidator


class Venue(models.Model):
    name = models.CharField(max_length=200, verbose_name='Tên nhà hát')
    address = models.TextField(verbose_name='Địa chỉ')
    phone = models.CharField(max_length=20, verbose_name='Điện thoại')
    email = models.EmailField(verbose_name='Email')
    description = models.TextField(blank=True, verbose_name='Mô tả')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Nhà hát'
        verbose_name_plural = 'Nhà hát'

    def __str__(self):
        return self.name


class Section(models.Model):
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE, related_name='sections')
    name = models.CharField(max_length=100, verbose_name='Tên khu vực')
    code = models.CharField(max_length=20, verbose_name='Mã khu vực')
    position_x = models.IntegerField(default=0, verbose_name='Vị trí X')
    position_y = models.IntegerField(default=0, verbose_name='Vị trí Y')
    order = models.IntegerField(default=0, verbose_name='Thứ tự')

    class Meta:
        verbose_name = 'Khu vực'
        verbose_name_plural = 'Khu vực'
        ordering = ['order']

    def __str__(self):
        return f"{self.venue.name} - {self.name}"


class PriceCategory(models.Model):
    name = models.CharField(max_length=100, verbose_name='Tên loại vé')
    code = models.CharField(max_length=20, unique=True, verbose_name='Mã')
    base_price = models.DecimalField(
        max_digits=10,
        decimal_places=0,
        validators=[MinValueValidator(0)],
        verbose_name='Giá cơ bản'
    )
    color = models.CharField(max_length=7, default='#CCCCCC', verbose_name='Màu hiển thị')

    class Meta:
        verbose_name = 'Loại giá vé'
        verbose_name_plural = 'Loại giá vé'

    def __str__(self):
        return f"{self.name} - {self.base_price:,.0f}đ"


class Row(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='rows')
    label = models.CharField(max_length=10, verbose_name='Nhãn hàng')
    seat_count = models.IntegerField(validators=[MinValueValidator(1)], verbose_name='Số ghế')
    position_y = models.IntegerField(default=0, verbose_name='Vị trí Y')
    price_category = models.ForeignKey(
        PriceCategory,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Loại giá'
    )

    class Meta:
        verbose_name = 'Hàng ghế'
        verbose_name_plural = 'Hàng ghế'
        ordering = ['position_y']

    def __str__(self):
        return f"{self.section.name} - Hàng {self.label}"


class Seat(models.Model):
    STATUS_CHOICES = [
        ('active', 'Hoạt động'),
        ('maintenance', 'Bảo trì'),
        ('disabled', 'Vô hiệu hóa'),
    ]

    row = models.ForeignKey(Row, on_delete=models.CASCADE, related_name='seats')
    number = models.IntegerField(verbose_name='Số ghế')
    position_x = models.IntegerField(default=0, verbose_name='Vị trí X')
    position_y = models.IntegerField(default=0, verbose_name='Vị trí Y')
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='active',
        verbose_name='Trạng thái'
    )
    is_accessible = models.BooleanField(default=False, verbose_name='Ghế cho người khuyết tật')

    class Meta:
        verbose_name = 'Ghế'
        verbose_name_plural = 'Ghế'
        unique_together = ['row', 'number']
        ordering = ['row', 'number']

    def __str__(self):
        return f"{self.row.label}{self.number}"

    @property
    def full_label(self):
        return f"{self.row.section.name} - {self.row.label}{self.number}"
