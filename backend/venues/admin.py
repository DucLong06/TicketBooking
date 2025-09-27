from .models import Venue, Section, PriceCategory, Row, Seat, VenueLayout, ContactInfo
from django.contrib import admin
from django.utils.html import format_html
from django.shortcuts import redirect
from django.urls import path, reverse
from django.http import JsonResponse
from django.db import models
from .venue_templates import VENUE_TEMPLATES


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
            layout.pk = None  # Reset primary key
            layout.name = f"{layout.name} (Copy)"
            layout.is_template = False
            layout.save()
        self.message_user(request, f"Đã sao chép {queryset.count()} layout")
    duplicate_layout.short_description = "Sao chép layout"


class RowInline(admin.TabularInline):
    model = Row
    extra = 1
    fields = ['label', 'seat_count', 'position_y', 'price_category']


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
            '<div style="width: 20px; height: 20px; background-color: {}; border: 1px solid #ccc;"></div>',
            obj.color
        )
    color_preview.short_description = 'Màu'


class SeatInline(admin.TabularInline):
    model = Seat
    extra = 0
    fields = ['number', 'position_x', 'position_y', 'status', 'is_accessible']
    readonly_fields = ['position_x', 'position_y']


@admin.register(Row)
class RowAdmin(admin.ModelAdmin):
    list_display = [
        'label', 'section', 'seat_count', 'actual_seats',
        'numbering_style', 'price_category'
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

    actions = ['regenerate_seats']

    def regenerate_seats(self, request, queryset):
        """Regenerate seats for selected rows"""
        for row in queryset:
            # Delete existing seats
            row.seats.all().delete()

            # Create new seats based on numbering system
            positions = row.actual_seat_positions
            for seat_num, pos in positions.items():
                Seat.objects.create(
                    row=row,
                    number=seat_num,
                    position_x=pos['x'],
                    position_y=pos['y'],
                    status='active'
                )

        self.message_user(request, f"Đã tạo lại ghế cho {queryset.count()} hàng")
    regenerate_seats.short_description = "Tạo lại ghế theo numbering system"


@admin.register(Seat)
class SeatAdmin(admin.ModelAdmin):
    list_display = ['full_label', 'row', 'status', 'is_accessible']  # full_label sẽ work sau khi sửa
    list_filter = ['status', 'is_accessible', 'row__section']
    search_fields = ['number', 'row__label', 'row__section__name']


@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'venue_type',
        'layout_name',
        'total_seats_display',
        'sections_count',
        'actions_column'
    ]
    list_filter = ['venue_type', 'layout']
    search_fields = ['name', 'address']
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        ('Thông tin cơ bản', {
            'fields': ('name', 'venue_type', 'address', 'phone', 'email')
        }),
        ('Layout', {
            'fields': ('layout', 'description')
        }),
        ('Thông tin khác', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                '<int:venue_id>/create-from-template/',
                self.admin_site.admin_view(self.create_from_template_view),
                name='venues_venue_create_from_template'
            ),
            path(
                '<int:venue_id>/preview/',
                self.admin_site.admin_view(self.preview_layout_view),
                name='venues_venue_preview_layout'
            ),
        ]
        return custom_urls + urls

    def layout_name(self, obj):
        return obj.layout.name if obj.layout else '-'
    layout_name.short_description = 'Layout Template'

    def total_seats_display(self, obj):
        total = obj.total_seats
        return format_html('<strong>{}</strong>', total)
    total_seats_display.short_description = 'Tổng ghế'

    def sections_count(self, obj):
        return obj.sections.count()
    sections_count.short_description = 'Số sections'

    def actions_column(self, obj):
        preview_url = reverse(
            'admin:venues_venue_preview_layout',
            args=[obj.pk]
        )
        create_url = reverse(
            'admin:venues_venue_create_from_template',
            args=[obj.pk]
        )
        return format_html(
            '<a class="button" href="{}">Preview</a> '
            '<a class="button" href="{}">From Template</a>',
            preview_url, create_url
        )
    actions_column.short_description = 'Actions'

    def create_from_template_view(self, request, venue_id):
        """View để tạo venue từ template"""
        # Implementation sẽ làm sau
        return JsonResponse({'status': 'success', 'message': 'Feature coming soon'})

    def preview_layout_view(self, request, venue_id):
        """View để preview layout"""
        # Implementation sẽ làm sau
        return JsonResponse({'status': 'success', 'message': 'Preview coming soon'})

    actions = ['clone_venue']

    def clone_venue(self, request, queryset):
        for venue in queryset:
            # Clone venue
            original_name = venue.name
            venue.pk = None
            venue.name = f"{original_name} (Copy)"
            venue.save()

            # TODO: Clone sections, rows, seats

        self.message_user(request, f"Đã sao chép {queryset.count()} venue")
    clone_venue.short_description = "Sao chép venue"


@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    """Admin for Contact Information - Singleton Model"""

    list_display = ['name', 'hotline_display_admin', 'support_email', 'social_links']

    fieldsets = (
        ('Thông tin cơ bản', {
            'fields': ('name', 'hotline', 'support_email'),
            'description': 'Thông tin liên hệ chính hiển thị trong email và website'
        }),
        ('Mạng xã hội', {
            'fields': ('facebook_url', 'tiktok_url', 'instagram_url', 'website_url'),
            'classes': ('collapse',),
        }),
        ('Branding', {
            'fields': ('logo_url', 'copyright_text'),
        }),
        ('Thông tin hệ thống', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        })
    )

    readonly_fields = ['created_at', 'updated_at']

    def hotline_display_admin(self, obj):
        """Display formatted hotline in admin list"""
        return obj.hotline_display
    hotline_display_admin.short_description = 'Hotline'

    def social_links(self, obj):
        """Display social media links as clickable icons"""
        links = []
        if obj.facebook_url:
            links.append(f'<a href="{obj.facebook_url}" target="_blank">📘 FB</a>')
        if obj.tiktok_url:
            links.append(f'<a href="{obj.tiktok_url}" target="_blank">🎵 TT</a>')
        if obj.instagram_url:
            links.append(f'<a href="{obj.instagram_url}" target="_blank">📷 IG</a>')
        if obj.website_url:
            links.append(f'<a href="{obj.website_url}" target="_blank">🌐 Web</a>')

        return format_html(' | '.join(links)) if links else '-'
    social_links.short_description = 'Mạng xã hội'

    def has_add_permission(self, request):
        """Only allow one ContactInfo instance"""
        return not ContactInfo.objects.exists()

    def has_delete_permission(self, request, obj=None):
        """Prevent deletion of ContactInfo"""
        return False

    def changelist_view(self, request, extra_context=None):
        """Redirect to edit if ContactInfo exists, otherwise show add form"""
        if ContactInfo.objects.exists():
            contact = ContactInfo.objects.first()
            return redirect('admin:venues_contactinfo_change', contact.pk)
        return super().changelist_view(request, extra_context)
