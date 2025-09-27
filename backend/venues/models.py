from django.db import models
from django.core.validators import MinValueValidator

VENUE_TYPES = [
    ('opera', 'Nhà hát Opera'),
    ('concert', 'Phòng hòa nhạc'),
    ('theater', 'Rạp hát'),
    ('cinema', 'Rạp chiếu phim'),
    ('stadium', 'Sân vận động'),
]


class VenueLayout(models.Model):
    """Template layout cho các loại nhà hát"""
    name = models.CharField(max_length=100, verbose_name='Tên layout')
    venue_type = models.CharField(
        max_length=20,
        choices=VENUE_TYPES,
        verbose_name='Loại nhà hát'
    )
    description = models.TextField(blank=True, verbose_name='Mô tả')
    config = models.JSONField(verbose_name='Cấu hình layout')
    is_template = models.BooleanField(default=True, verbose_name='Là template')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Layout nhà hát'
        verbose_name_plural = 'Layout nhà hát'

    def __str__(self):
        return f"{self.name} ({self.get_venue_type_display()})"

    @property
    def total_seats(self):
        """Tính tổng số ghế từ config"""
        total = 0
        for floor in self.config.get('floors', []):
            for section in floor.get('sections', []):
                for row in section.get('rows', []):
                    total += row.get('seats', 0)
        return total


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
    layout = models.ForeignKey(
        VenueLayout,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Layout template'
    )
    venue_type = models.CharField(
        max_length=20,
        choices=VENUE_TYPES,
        default='theater',
        verbose_name='Loại nhà hát'
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

    @property
    def total_seats(self):
        """Tính tổng số ghế trong venue"""
        total = 0
        for section in self.sections.all():
            total += section.rows.aggregate(
                count=models.Count('seats')
            )['count'] or 0
        return total


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
    NUMBERING_CHOICES = [
        ('left_to_right', 'Trái sang Phải (1,2,3,4...)'),
        ('center_out', 'Giữa ra Ngoài (lẻ trái, chẵn phải)'),
        ('right_to_left', 'Phải sang Trái'),
        ('vertical', 'Dọc (cho LG boxes)'),
    ]

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

    # NEW FIELDS
    numbering_style = models.CharField(
        max_length=20,
        choices=NUMBERING_CHOICES,
        default='center_out',
        verbose_name='Kiểu đánh số ghế'
    )
    center_x = models.IntegerField(
        default=400,
        verbose_name='Vị trí trung tâm X (cho center_out)'
    )
    aisle_width = models.IntegerField(
        default=60,
        verbose_name='Độ rộng lối đi giữa'
    )
    has_center_aisle = models.BooleanField(
        default=True,
        verbose_name='Có lối đi giữa'
    )
    gaps = models.JSONField(
        default=list,
        blank=True,
        verbose_name='Vị trí ghế bị ẩn/lối đi',
        help_text='Danh sách số ghế bị ẩn để tạo lối đi. VD: [8,9,26,27]'
    )

    class Meta:
        verbose_name = 'Hàng ghế'
        verbose_name_plural = 'Hàng ghế'
        ordering = ['position_y']

    def __str__(self):
        return f"{self.section.name} - Hàng {self.label}"

    @property
    def actual_seat_positions(self):
        """Tính toán vị trí thực tế của ghế theo numbering system"""
        if self.numbering_style == 'center_out':
            return self._calculate_center_out_positions()
        elif self.numbering_style == 'left_to_right':
            return self._calculate_left_to_right_positions()
        elif self.numbering_style == 'vertical':
            return self._calculate_vertical_positions()
        else:
            return self._calculate_left_to_right_positions()

    def _calculate_center_out_positions(self):
        """Tính vị trí cho center-out numbering WITH GAPS"""
        positions = {}
        seat_width = 22
        gaps = set(self.gaps) if self.gaps else set()

        # 🔧 FIX: Chỉ process seats KHÔNG trong gaps
        available_seats = []
        for i in range(1, self.seat_count + 1):
            if i not in gaps:
                available_seats.append(i)

        # Chia odd/even từ available_seats
        left_seats = [s for s in available_seats if s % 2 == 1]
        right_seats = [s for s in available_seats if s % 2 == 0]

        # Sort for center-out
        left_seats.sort(reverse=True)  # 19,17,15,13,11,9,7,5,3,1
        right_seats.sort()              # 2,4,6,8,10,12,14,16,18,20

        # Calculate positions
        for idx, seat_num in enumerate(left_seats):
            x = self.center_x - (self.aisle_width // 2) - (idx + 1) * seat_width
            positions[seat_num] = {'x': x, 'y': self.position_y}

        for idx, seat_num in enumerate(right_seats):
            x = self.center_x + (self.aisle_width // 2) + (idx + 1) * seat_width
            positions[seat_num] = {'x': x, 'y': self.position_y}

        return positions

    def _calculate_left_to_right_positions(self):
        """Tính vị trí cho left-to-right numbering"""
        positions = {}
        seat_width = 22
        start_x = self.center_x - (self.seat_count * seat_width // 2)
        gaps = set(self.gaps) if self.gaps else set()

        seat_index = 0
        for seat_num in range(1, self.seat_count + 1):
            if seat_num not in gaps:
                x = start_x + seat_index * seat_width
                positions[seat_num] = {'x': x, 'y': self.position_y}
                seat_index += 1

        return positions

    def _calculate_vertical_positions(self):
        """Tính vị trí cho vertical numbering (LG boxes)"""
        positions = {}
        seat_height = 25

        for seat_num in range(1, self.seat_count + 1):
            x = self.center_x  # Same X for vertical
            y = self.position_y + (seat_num - 1) * seat_height
            positions[seat_num] = {'x': x, 'y': y}

        return positions


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
        return f"{self.row.section.name}-{self.row.label}{self.number}"

    @property
    def seat_code(self):
        return f"{self.row.label}{self.number}"

    @property
    def full_label(self):
        """For backward compatibility with existing admin"""
        return f"{self.row.label}{self.number}"
