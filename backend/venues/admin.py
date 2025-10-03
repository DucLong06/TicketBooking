from django.contrib import admin
from django.utils.html import format_html
from django.shortcuts import redirect
from django.urls import path, reverse
from django.http import JsonResponse
from django.db import models
from .models import Venue, Section, PriceCategory, Row, Seat, VenueLayout, ContactInfo


@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    list_display = ['name', 'hotline', 'support_email']

    fieldsets = (
        ('Thông tin cơ bản', {
            'fields': ('name', 'hotline', 'support_email')
        }),
        ('Social Media', {
            'fields': ('facebook_url', 'tiktok_url', 'instagram_url', 'website_url')
        }),
        ('Branding', {
            'fields': ('logo_url', 'copyright_text')
        }),
    )

    def has_add_permission(self, request):
        # Only allow one instance
        return not ContactInfo.objects.exists()

    def has_delete_permission(self, request, obj=None):
        # Don't allow deletion
        return False


@admin.register(VenueLayout)
class VenueLayoutAdmin(admin.ModelAdmin):
    list_display = ['name', 'venue_type', 'total_seats', 'is_template', 'created_at']
    list_filter = ['venue_type', 'is_template']
    search_fields = ['name', 'description']
    readonly_fields = ['total_seats', 'created_at', 'updated_at']

    fieldsets = (
        ('Thông tin cơ bản', {
            'fields': ('name', 'venue_type', 'description', 'is_template')
        }),
        ('Cấu hình Layout', {
            'fields': ('config',),
            'description': 'JSON config cho layout. Xem venue_templates.py để biết format.'
        }),
        ('Thông tin khác', {
            'fields': ('total_seats', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

    def total_seats(self, obj):
        return obj.total_seats
    total_seats.short_description = 'Tổng số ghế'

    actions = ['duplicate_layout']

    def duplicate_layout(self, request, queryset):
        for layout in queryset:
            layout.pk = None
            layout.name = f"{layout.name} (Copy)"
            layout.is_template = False
            layout.save()
        self.message_user(request, f"Đã sao chép {queryset.count()} layout")
    duplicate_layout.short_description = "Sao chép layout"


class RowInline(admin.TabularInline):
    model = Row
    extra = 1
    fields = ['label', 'seat_count', 'position_y', 'price_category', 'numbering_style']


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ['name', 'venue', 'code', 'total_seats', 'order']
    list_filter = ['venue']
    search_fields = ['name', 'code']
    inlines = [RowInline]
    ordering = ['venue', 'order']

    def total_seats(self, obj):
        return obj.rows.aggregate(
            total=models.Sum('seat_count')
        )['total'] or 0
    total_seats.short_description = 'Tổng ghế'


@admin.register(PriceCategory)
class PriceCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'base_price', 'color_preview']
    search_fields = ['name', 'code']

    def color_preview(self, obj):
        return format_html(
            '<div style="width: 30px; height: 20px; background-color: {}; border: 1px solid #ccc; border-radius: 3px;"></div>',
            obj.color
        )
    color_preview.short_description = 'Màu'


class SeatInline(admin.TabularInline):
    model = Seat
    extra = 0
    fields = [
        'number',
        'display_number',
        'price_category',
        'seat_image',
        'spacing_after',
        'status',
        'is_accessible'
    ]
    readonly_fields = ['number']
    autocomplete_fields = ['price_category']


@admin.register(Row)
class RowAdmin(admin.ModelAdmin):
    list_display = [
        'label',
        'section',
        'seat_count',
        'actual_seats',
        'numbering_style',
        'price_category'
    ]
    list_filter = ['section__venue', 'section', 'price_category', 'numbering_style']
    search_fields = ['label']
    inlines = [SeatInline]

    fieldsets = (
        ('Thông tin cơ bản', {
            'fields': ('section', 'label', 'seat_count', 'position_y', 'price_category')
        }),
        ('Hệ thống đánh số ghế', {
            'fields': ('numbering_style', 'center_x', 'aisle_width', 'has_center_aisle', 'gaps'),
            'description': 'Cấu hình cách đánh số và sắp xếp ghế'
        })
    )

    def actual_seats(self, obj):
        count = obj.seats.count()
        expected = obj.seat_count
        color = 'green' if count == expected else 'red'
        return format_html(
            '<span style="color: {};">{}/{}</span>',
            color, count, expected
        )
    actual_seats.short_description = 'Ghế thực tế/Dự kiến'

    actions = ['regenerate_seats', 'create_default_seats', 'add_center_spacing']

    def regenerate_seats(self, request, queryset):
        """Regenerate seats for selected rows"""
        for row in queryset:
            row.seats.all().delete()

            positions = row.actual_seat_positions
            for seat_num, pos in positions.items():
                Seat.objects.create(
                    row=row,
                    number=str(seat_num),
                    display_number=str(seat_num),
                    position_x=pos['x'],
                    position_y=pos['y'],
                    price_category=row.price_category,
                    status='active'
                )

        self.message_user(request, f"Đã tạo lại ghế cho {queryset.count()} hàng")
    regenerate_seats.short_description = "Tạo lại ghế theo numbering system"

    def create_default_seats(self, request, queryset):
        """Tạo ghế mặc định cho hàng đã chọn"""
        total = 0
        for row in queryset:
            count = row.create_default_seats()
            total += count

        self.message_user(
            request,
            f"Đã tạo {total} ghế cho {queryset.count()} hàng"
        )
    create_default_seats.short_description = "Tạo ghế mặc định (auto)"

    def add_center_spacing(self, request, queryset):
        """Thêm spacing ở giữa hàng"""
        for row in queryset:
            seats = list(row.seats.all().order_by('number'))
            if not seats:
                continue

            midpoint = len(seats) // 2
            if midpoint > 0 and midpoint < len(seats):
                seat = seats[midpoint - 1]
                seat.spacing_after = 40  # 40px gap
                seat.save()

        self.message_user(request, f"Đã thêm spacing cho {queryset.count()} hàng")
    add_center_spacing.short_description = "Thêm khoảng trống giữa hàng"


@admin.register(Seat)
class SeatAdmin(admin.ModelAdmin):
    list_display = [
        'full_display_label',
        'number',
        'display_number',
        'row',
        'price_category_display',
        'image_preview',
        'spacing_after',
        'status',
        'is_accessible'
    ]
    list_filter = [
        'status',
        'is_accessible',
        'row__section',
        'price_category'
    ]
    search_fields = ['number', 'display_number', 'row__label']

    list_editable = ['display_number', 'spacing_after']

    autocomplete_fields = ['row', 'price_category']

    fieldsets = (
        ('Thông tin cơ bản', {
            'fields': ('row', 'number', 'display_number', 'status')
        }),
        ('Giá và hiển thị', {
            'fields': ('price_category', 'spacing_after', 'seat_image', 'seat_image_preview'),
            'description': 'Price category để trống sẽ lấy từ hàng. Spacing_after để tạo khoảng trống.'
        }),
        ('Vị trí', {
            'fields': ('position_x', 'position_y', 'is_accessible')
        })
    )

    readonly_fields = ['seat_image_preview']

    def price_category_display(self, obj):
        """Hiển thị price category với màu"""
        pc = obj.effective_price_category
        if not pc:
            return '-'
        return format_html(
            '<span style="display:inline-block; width:12px; height:12px; background-color:{}; border:1px solid #ccc; margin-right:5px; border-radius:2px;"></span>{}',
            pc.color,
            pc.name
        )
    price_category_display.short_description = 'Loại giá'

    def image_preview(self, obj):
        """Preview ảnh ghế trong admin list"""
        if obj.seat_image:
            return format_html(
                '<img src="{}" style="width: 50px; height: 50px; object-fit: cover; border-radius: 4px; border: 1px solid #ddd;" />',
                obj.seat_image.url
            )
        return format_html('<span style="color: #999;">Chưa có ảnh</span>')
    image_preview.short_description = 'Ảnh'

    def seat_image_preview(self, obj):
        """Preview ảnh ghế lớn hơn trong detail page"""
        if obj.seat_image:
            return format_html(
                '<img src="{}" style="max-width: 300px; max-height: 300px; object-fit: contain; border-radius: 8px; border: 2px solid #ddd; box-shadow: 0 2px 4px rgba(0,0,0,0.1);" />',
                obj.seat_image.url
            )
        return format_html('<p style="color: #999; font-style: italic;">Chưa có ảnh</p>')
    seat_image_preview.short_description = 'Preview ảnh'


@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'venue_type',
        'layout_name',
        'layout_image_preview',
        'total_seats_display',
        'sections_count',
        'is_active'
    ]
    list_filter = ['venue_type', 'layout', 'is_active']
    search_fields = ['name', 'address', 'code']
    readonly_fields = ['created_at', 'updated_at', 'code', 'layout_image_preview_large']

    fieldsets = (
        ('Thông tin cơ bản', {
            'fields': ('name', 'code', 'venue_type', 'address', 'is_active')
        }),
        ('Layout', {
            'fields': ('layout', 'layout_image', 'layout_image_preview_large', 'description')
        }),
        ('Liên hệ (Legacy)', {
            'fields': ('phone', 'email', 'hotline', 'support_email'),
            'classes': ('collapse',),
            'description': 'Các field này để tương thích ngược. Nên dùng ContactInfo thay vì.'
        }),
        ('Social Media (Legacy)', {
            'fields': ('facebook_url', 'tiktok_url', 'instagram_url', 'website_url', 'logo_url', 'copyright_text'),
            'classes': ('collapse',)
        }),
        ('Cài đặt', {
            'fields': ('checkin_minutes_before',)
        }),
        ('Thông tin khác', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

    def layout_name(self, obj):
        return obj.layout.name if obj.layout else '-'
    layout_name.short_description = 'Layout Template'

    def layout_image_preview(self, obj):
        """Preview ảnh layout nhỏ trong list"""
        if obj.layout_image:
            return format_html(
                '<img src="{}" style="width: 60px; height: 40px; object-fit: cover; border-radius: 4px; border: 1px solid #ddd;" />',
                obj.layout_image.url
            )
        return format_html('<span style="color: #999; font-size: 11px;">Chưa có</span>')
    layout_image_preview.short_description = 'Layout'

    def layout_image_preview_large(self, obj):
        """Preview ảnh layout lớn trong detail page"""
        if obj.layout_image:
            return format_html(
                '<div style="margin: 10px 0;">'
                '<img src="{}" style="max-width: 600px; max-height: 400px; object-fit: contain; border-radius: 8px; border: 2px solid #ddd; box-shadow: 0 2px 8px rgba(0,0,0,0.1);" />'
                '<p style="margin-top: 10px; color: #666; font-size: 12px;">💡 Ảnh này sẽ hiển thị trên trang chọn ghế</p>'
                '</div>',
                obj.layout_image.url
            )
        return format_html(
            '<div style="padding: 20px; background: #f9f9f9; border-radius: 8px; text-align: center;">'
            '<p style="color: #999; font-style: italic;">Chưa có ảnh layout</p>'
            '<p style="color: #666; font-size: 12px; margin-top: 5px;">Upload ảnh sơ đồ nhà hát để khách hàng dễ hình dung</p>'
            '</div>'
        )
    layout_image_preview_large.short_description = 'Preview Layout'

    def total_seats_display(self, obj):
        total = obj.total_seats
        return format_html('<strong style="color: #2563eb;">{}</strong>', total)
    total_seats_display.short_description = 'Tổng ghế'

    def sections_count(self, obj):
        return obj.sections.count()
    sections_count.short_description = 'Số khu vực'
