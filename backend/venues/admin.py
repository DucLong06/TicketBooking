from django.contrib import admin
from django.utils.html import format_html
from .models import Venue, Section, Row, Seat, PriceCategory, ContactInfo


@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    list_display = ['name', 'hotline_display', 'support_email', 'updated_at']
    fieldsets = (
        ('Thông tin cơ bản', {
            'fields': ('name', 'logo_url', 'copyright_text')
        }),
        ('Liên hệ', {
            'fields': ('hotline', 'support_email')
        }),
        ('Mạng xã hội', {
            'fields': ('facebook_url', 'tiktok_url', 'instagram_url', 'website_url')
        }),
    )

    def has_add_permission(self, request):
        # Only allow one instance
        return not ContactInfo.objects.exists()

    def has_delete_permission(self, request, obj=None):
        # Don't allow deletion
        return False


@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    # Keep original fields but add new ones
    list_display = ['name', 'address', 'capacity', 'is_active', 'hotline_display']
    list_filter = ['is_active']
    search_fields = ['name', 'address']
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        ('Thông tin cơ bản', {
            'fields': ('name', 'code', 'address', 'capacity', 'layout_image', 'is_active')
        }),
        ('Cài đặt', {
            'fields': ('checkin_minutes_before',)
        }),
        ('Thông tin liên hệ (Optional)', {
            'fields': ('hotline', 'support_email', 'logo_url', 'copyright_text'),
            'classes': ('collapse',)
        }),
        ('Mạng xã hội (Optional)', {
            'fields': ('facebook_url', 'tiktok_url', 'instagram_url', 'website_url'),
            'classes': ('collapse',)
        }),
    )

    def hotline_display(self, obj):
        return obj.hotline_display if hasattr(obj, 'hotline_display') else getattr(obj, 'phone', '')
    hotline_display.short_description = 'Hotline'


class RowInline(admin.TabularInline):
    model = Row
    extra = 1


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    # Match current structure
    list_display = ['name', 'venue', 'code', 'position_x', 'position_y']
    list_filter = ['venue']
    search_fields = ['name', 'code']
    inlines = [RowInline]
    ordering = ['venue', 'name']


@admin.register(PriceCategory)
class PriceCategoryAdmin(admin.ModelAdmin):
    # Keep original structure
    list_display = ['name', 'code', 'base_price', 'color_display']
    search_fields = ['name', 'code']

    def color_display(self, obj):
        return format_html(
            '<span style="background-color: {}; padding: 5px 10px; color: white; border-radius: 3px;">{}</span>',
            obj.color,
            obj.color
        )
    color_display.short_description = 'Màu sắc'


class SeatInline(admin.TabularInline):
    model = Seat
    extra = 0
    fields = ['number', 'position_x', 'position_y', 'status', 'is_accessible']


@admin.register(Row)
class RowAdmin(admin.ModelAdmin):
    # Use original structure
    list_display = ['label', 'section', 'seat_count', 'price_category']
    list_filter = ['section__venue', 'section', 'price_category']
    search_fields = ['label']
    inlines = [SeatInline]


@admin.register(Seat)
class SeatAdmin(admin.ModelAdmin):
    list_display = ['full_label', 'row', 'number', 'status', 'is_accessible']
    list_filter = ['row__section__venue', 'row__section', 'status', 'is_accessible']
    search_fields = ['row__label', 'number']
    list_editable = ['status']
