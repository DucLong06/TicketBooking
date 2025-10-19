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

    rules = models.TextField(
        blank=True,
        verbose_name='Quy định và lưu ý',
        help_text='Các quy định, lưu ý quan trọng cho khách hàng. Mỗi quy định nên viết trên 1 dòng.'
    )

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
        if not hasattr(self, '_total_seats_cache'):
            from venues.models import Seat
            self._total_seats_cache = Seat.objects.filter(
                row__section__venue=self,
                status='active'
            ).count()
        return self._total_seats_cache


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
        max_length=500,
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
    name = models.TextField(verbose_name='Tên loại vé')
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

    spacing_after = models.IntegerField(
        default=0,
        verbose_name='Khoảng cách sau hàng (px)',
        help_text='Khoảng trống sau hàng này (để tạo lối đi giữa các nhóm hàng)'
    )

    price_category = models.ForeignKey(
        PriceCategory,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Loại giá'
    )

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
        if self.numbering_style == 'center_out':
            return self._calculate_center_out_positions()
        elif self.numbering_style == 'left_to_right':
            return self._calculate_left_to_right_positions()
        elif self.numbering_style == 'vertical':
            return self._calculate_vertical_positions()
        else:
            return self._calculate_left_to_right_positions()

    def _calculate_center_out_positions(self):
        positions = {}
        seat_width = 22
        gaps = set(self.gaps) if self.gaps else set()

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

    def create_default_seats(self):
        from venues.models import Seat

        self.seats.all().delete()

        positions = self.actual_seat_positions

        for seat_num, pos in positions.items():
            if seat_num in (self.gaps or []):
                continue

            Seat.objects.create(
                row=self,
                number=str(seat_num),              # BE number
                display_number=str(seat_num),      # FE display (ban đầu giống BE)
                position_x=pos['x'],
                position_y=pos['y'],
                price_category=self.price_category,  # Inherit từ row
                spacing_after=0,                   # Không có spacing
                status='active'
            )

        return self.seats.count()


class Seat(models.Model):
    STATUS_CHOICES = [
        ('active', 'Hoạt động'),
        ('broken', 'Hỏng'),
        ('maintenance', 'Bảo trì'),
        ('reserved', 'Để dành'),
    ]

    row = models.ForeignKey(Row, on_delete=models.CASCADE, related_name='seats')
    number = models.CharField(max_length=10, verbose_name='Số ghế')

    display_number = models.CharField(
        max_length=10,
        verbose_name='Số hiển thị',
        help_text='Số ghế hiển thị trên FE (có thể khác với number trong BE)',
        blank=True,
        null=True
    )

    position_x = models.IntegerField(default=0, verbose_name='Vị trí X')
    position_y = models.IntegerField(default=0, verbose_name='Vị trí Y')

    price_category = models.ForeignKey(
        PriceCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Loại giá',
        help_text='Để trống sẽ lấy từ hàng ghế'
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='active',
        verbose_name='Trạng thái'
    )

    spacing_after = models.IntegerField(
        default=0,
        verbose_name='Khoảng cách sau ghế (px)',
        help_text='Khoảng trống sau ghế này (không ẩn ghế)'
    )

    seat_image = models.ImageField(
        upload_to='seats/',
        blank=True,
        null=True,
        verbose_name='Ảnh ghế thực tế',
        help_text='Ảnh chụp ghế thực tế để khách hàng xem'
    )

    is_accessible = models.BooleanField(default=False, verbose_name='Ghế người khuyết tật')

    class Meta:
        verbose_name = 'Ghế'
        verbose_name_plural = 'Ghế'
        unique_together = ['row', 'number']
        ordering = ['row', 'number']

    def __str__(self):
        return f"{self.row.section.name}-{self.row.label}{self.display_label}"

    @property
    def display_label(self):
        return self.display_number if self.display_number else self.number

    @property
    def effective_price_category(self):
        """Price category thực tế của ghế"""
        return self.price_category if self.price_category else self.row.price_category

    @property
    def seat_code(self):
        return f"{self.row.label}{self.display_label}"

    @property
    def full_label(self):
        """For backward compatibility"""
        return f"{self.row.label}{self.display_label}"

    @property
    def full_display_label(self):
        return f"{self.row.label}{self.display_label}"

    @property
    def full_display_label_with_section(self):
        return f"{self.row.section.name} - {self.row.label}{self.display_label}"

    @property
    def section_name(self):
        return self.row.section.name
