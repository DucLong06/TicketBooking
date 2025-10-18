from django.contrib import admin
from django.utils.html import format_html
from django import forms
from datetime import datetime, timedelta
from django.utils import timezone
from .models import Show, Performance, PerformancePrice, Poster
from venues.models import PriceCategory
from markdownx.admin import MarkdownxModelAdmin


class QuickPerformanceInlineForm(forms.ModelForm):
    create_multiple = forms.BooleanField(
        required=False,
        label='Tạo nhiều suất',
        help_text='Tạo nhiều suất diễn cho nhiều ngày'
    )
    days_count = forms.IntegerField(
        required=False,
        initial=7,
        label='Số ngày',
        help_text='Tạo suất diễn trong bao nhiêu ngày'
    )
    time_slots = forms.CharField(
        required=False,
        initial='19:00,21:00',
        label='Giờ diễn',
        help_text='Các giờ diễn, cách nhau bởi dấu phẩy (VD: 19:00,21:00)'
    )

    class Meta:
        model = Performance
        fields = ['datetime', 'status']


class PerformanceInline(admin.TabularInline):
    model = Performance
    form = QuickPerformanceInlineForm
    extra = 1
    fields = ['datetime', 'status']

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        if not change:  # Only for new performances
            price_categories = PriceCategory.objects.all()
            for category in price_categories:
                PerformancePrice.objects.get_or_create(
                    performance=obj,
                    price_category=category,
                    defaults={'price': category.base_price}
                )


@admin.register(Show)
class ShowAdmin(MarkdownxModelAdmin):
    list_display = ['name', 'category', 'venue', 'duration_minutes', 'is_active', 'created_at']
    list_filter = ['is_active', 'category', 'venue', 'created_at']
    search_fields = ['name', 'category', 'description']
    prepopulated_fields = {'slug': ('name',)}

    fieldsets = (
        ('Thông tin cơ bản', {
            'fields': ('name', 'slug', 'category', 'duration_minutes', 'venue', 'poster')
        }),
        ('Nội dung', {
            'fields': ('description', 'description_markdown', 'trailer_url')
        }),
        ('Cài đặt', {
            'fields': ('service_fee_per_ticket', 'is_active')
        }),
    )

    class Media:
        css = {
            'all': ('markdownx/admin/css/markdownx.min.css',)
        }
        js = (
            'markdownx/js/markdownx.min.js',
        )


@admin.register(Performance)
class SimplePerformanceAdmin(admin.ModelAdmin):
    list_display = ['show', 'datetime', 'status', 'available_seats_count', 'quick_actions']
    list_filter = ['show', 'status', 'datetime']
    list_editable = ['status']
    date_hierarchy = 'datetime'

    def quick_actions(self, obj):
        return format_html(
            '<a class="button" href="/admin/shows/performance/{}/change/">Sửa</a> '
            '<a class="button" href="/api/performances/{}/seat-map/" target="_blank">Xem sơ đồ</a>',
            obj.id, obj.id
        )
    quick_actions.short_description = 'Thao tác'

    actions = ['set_on_sale', 'set_sold_out', 'duplicate_performance']

    def set_on_sale(self, request, queryset):
        queryset.update(status='on_sale')
    set_on_sale.short_description = "Mở bán"

    def set_sold_out(self, request, queryset):
        queryset.update(status='sold_out')
    set_sold_out.short_description = "Hết vé"

    def duplicate_performance(self, request, queryset):
        """Duplicate selected performances to next day"""
        for perf in queryset:
            new_datetime = perf.datetime + timedelta(days=1)
            new_perf = Performance.objects.create(
                show=perf.show,
                datetime=new_datetime,
                status='on_sale'
            )

            # Copy prices
            for price in perf.prices.all():
                PerformancePrice.objects.create(
                    performance=new_perf,
                    price_category=price.price_category,
                    price=price.price
                )

        self.message_user(request, f"Đã nhân bản {queryset.count()} suất diễn sang ngày tiếp theo")
    duplicate_performance.short_description = "Nhân bản sang ngày tiếp theo"


@admin.register(Poster)
class PosterAdmin(admin.ModelAdmin):
    list_display = ['title', 'show', 'order', 'is_active', 'poster_preview', 'created_at']
    list_filter = ['is_active', 'show']
    search_fields = ['title', 'show__name']
    list_editable = ['order', 'is_active']
    ordering = ['order', '-created_at']

    fieldsets = (
        ('Thông tin cơ bản', {
            'fields': ('title', 'show', 'image')
        }),
        ('Cấu hình hiển thị', {
            'fields': ('order', 'is_active')
        }),
    )

    readonly_fields = ['created_at', 'updated_at']

    def poster_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height: 50px; max-width: 100px; object-fit: cover;" />',
                obj.image.url
            )
        return "Chưa có ảnh"
    poster_preview.short_description = 'Preview'
