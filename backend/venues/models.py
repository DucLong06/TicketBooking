from django.db import models
from django.core.validators import MinValueValidator


class Venue(models.Model):
    name = models.CharField(max_length=200, verbose_name='Tên địa điểm')
    code = models.CharField(max_length=20, unique=True, verbose_name='Mã địa điểm', blank=True)
    address = models.TextField(verbose_name='Địa chỉ')
    capacity = models.IntegerField(verbose_name='Sức chứa', default=0)
    layout_image = models.ImageField(
        upload_to='venues/layouts/',
        blank=True,
        null=True,
        verbose_name='Hình layout'
    )
    is_active = models.BooleanField(default=True, verbose_name='Đang hoạt động')
    description = models.TextField(blank=True, verbose_name='Mô tả')

    # Keep old fields for backward compatibility
    phone = models.CharField(max_length=20, blank=True, verbose_name='Điện thoại')
    email = models.EmailField(blank=True, verbose_name='Email')

    # New contact information
    hotline = models.CharField(max_length=20, blank=True, verbose_name='Hotline')
    support_email = models.EmailField(blank=True, verbose_name='Email hỗ trợ')
    facebook_url = models.URLField(blank=True, verbose_name='Facebook URL')
    tiktok_url = models.URLField(blank=True, verbose_name='TikTok URL')
    instagram_url = models.URLField(blank=True, verbose_name='Instagram URL')
    website_url = models.URLField(blank=True, verbose_name='Website URL')
    logo_url = models.URLField(blank=True, verbose_name='Logo URL')
    copyright_text = models.CharField(max_length=100, blank=True, verbose_name='Copyright text')
    # Check-in settings
    checkin_minutes_before = models.IntegerField(default=45, verbose_name='Check-in trước bao nhiêu phút')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Nhà hát'
        verbose_name_plural = 'Nhà hát'
        ordering = ['name']

    def save(self, *args, **kwargs):
        # Auto-generate code if not provided
        if not self.code:
            import re
            self.code = re.sub(r'[^a-zA-Z0-9]', '', self.name.lower())[:20]

        # Sync hotline with phone for backward compatibility
        if self.hotline and not self.phone:
            self.phone = self.hotline
        if self.phone and not self.hotline:
            self.hotline = self.phone

        # Sync support_email with email
        if self.support_email and not self.email:
            self.email = self.support_email
        if self.email and not self.support_email:
            self.support_email = self.email

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    @property
    def hotline_display(self):
        """Format hotline for display"""
        phone = self.hotline or self.phone
        if not phone:
            return ''
        # Format 0962989856 -> 0962.98.98.56
        phone = phone.replace(' ', '').replace('.', '').replace('-', '')
        if len(phone) == 10 and phone.startswith('0'):
            return f"{phone[:4]}.{phone[4:6]}.{phone[6:8]}.{phone[8:]}"
        return phone

    @property
    def maps_url(self):
        """Generate Google Maps URL"""
        return f"https://www.google.com/maps?q={self.address.replace(' ', '+')}"


class ContactInfo(models.Model):
    """Global contact information - singleton model"""
    name = models.CharField(max_length=100, default='Theater Booking', verbose_name='Tên tổ chức')
    hotline = models.CharField(max_length=20, verbose_name='Hotline')
    support_email = models.EmailField(verbose_name='Email hỗ trợ')
    facebook_url = models.URLField(blank=True, verbose_name='Facebook URL')
    tiktok_url = models.URLField(blank=True, verbose_name='TikTok URL')
    instagram_url = models.URLField(blank=True, verbose_name='Instagram URL')
    website_url = models.URLField(blank=True, verbose_name='Website URL')
    logo_url = models.URLField(
        default='https://lh3.googleusercontent.com/pw/AP1GczOeY1ZKKsObbQ5Em5H14byD0GRz_-ydPBGZWzBOQbun4cB783CMb3NsYbucZAmrMlCE-YJ8r3Ll71Fthb-wyaMjuQbPTc1jAPLcf-3-NzjBqBuS_3NB2W6JzfAWZP3sRYBVzVxethfg4iJBam3EhoDp=w489-h301-s-no-gm',
        verbose_name='Logo URL'
    )
    copyright_text = models.CharField(
        max_length=100,
        default='GMCP by duongcamart',
        verbose_name='Copyright text'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Thông tin liên hệ'
        verbose_name_plural = 'Thông tin liên hệ'

    def save(self, *args, **kwargs):
        # Ensure only one instance exists
        if not self.pk and ContactInfo.objects.exists():
            raise ValueError('ContactInfo is a singleton model. Only one instance is allowed.')
        super().save(*args, **kwargs)

    @classmethod
    def get_instance(cls):
        """Get the singleton instance"""
        obj, created = cls.objects.get_or_create(
            pk=1,
            defaults={
                'name': 'Theater Booking',
                'hotline': '0962989856',
                'support_email': 'duongcamart@gmail.com',
                'facebook_url': 'https://www.facebook.com/nhackichgiacmochipheo',
                'tiktok_url': 'https://www.tiktok.com/@giacmo.chipheo',
                'copyright_text': 'GMCP by duongcamart'
            }
        )
        return obj

    @property
    def hotline_display(self):
        """Format hotline for display"""
        if not self.hotline:
            return ''
        # Format 0962989856 -> 0962.98.98.56
        phone = self.hotline.replace(' ', '').replace('.', '').replace('-', '')
        if len(phone) == 10 and phone.startswith('0'):
            return f"{phone[:4]}.{phone[4:6]}.{phone[6:8]}.{phone[8:]}"
        return self.hotline

    def __str__(self):
        return self.name


# Rest of the models remain the same...
class Section(models.Model):
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE, related_name='sections')
    name = models.CharField(max_length=100, verbose_name='Tên khu vực')
    code = models.CharField(max_length=20, verbose_name='Mã khu vực')
    position_x = models.IntegerField(default=0, verbose_name='Vị trí X')
    position_y = models.IntegerField(default=0, verbose_name='Vị trí Y')
    order = models.IntegerField(default=0, verbose_name='Thứ tự')  # Keep for backward compatibility

    class Meta:
        verbose_name = 'Khu vực'
        verbose_name_plural = 'Khu vực'
        unique_together = ['venue', 'code']
        ordering = ['order']  # Keep original ordering

    def __str__(self):
        return f"{self.venue.name} - {self.name}"


class PriceCategory(models.Model):
    # Keep as global model - no venue field for backward compatibility
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
    label = models.CharField(max_length=10, verbose_name='Nhãn hàng')  # Keep original field
    name = models.CharField(max_length=10, verbose_name='Tên hàng', blank=True)  # Add for compatibility
    seat_count = models.IntegerField(validators=[MinValueValidator(1)], verbose_name='Số ghế')  # Keep original
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
        ordering = ['label']

    def save(self, *args, **kwargs):
        # Auto-sync name and label for backward compatibility
        if not self.name:
            self.name = self.label
        if not self.label:
            self.label = self.name
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.section.name} - Hàng {self.label}"


class Seat(models.Model):
    STATUS_CHOICES = [
        ('active', 'Hoạt động'),
        ('broken', 'Hỏng'),
        ('maintenance', 'Bảo trì'),
        ('reserved', 'Để dành'),
    ]

    row = models.ForeignKey(Row, on_delete=models.CASCADE, related_name='seats')
    number = models.CharField(max_length=10, verbose_name='Số ghế')
    position_x = models.IntegerField(default=0, verbose_name='Vị trí X')
    position_y = models.IntegerField(default=0, verbose_name='Vị trí Y')
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='active',
        verbose_name='Trạng thái'
    )
    is_accessible = models.BooleanField(default=False, verbose_name='Ghế người khuyết tật')

    class Meta:
        verbose_name = 'Ghế'
        verbose_name_plural = 'Ghế'
        unique_together = ['row', 'number']
        ordering = ['row', 'number']

    def __str__(self):
        return f"{self.row.section.name}-{self.row.name}{self.number}"

    @property
    def seat_code(self):
        return f"{self.row.name}{self.number}"

    @property
    def full_label(self):
        """For backward compatibility with existing admin"""
        return f"{self.row.name}{self.number}"
