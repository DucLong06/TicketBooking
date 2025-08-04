from django.contrib import admin
from django.utils.html import format_html
from django import forms
from datetime import datetime, timedelta
from django.utils import timezone
from .models import Show, Performance, PerformancePrice
from venues.models import PriceCategory


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

        # Auto create prices với giá mặc định
        if not change:  # Only for new performances
            price_categories = PriceCategory.objects.all()
            for category in price_categories:
                PerformancePrice.objects.get_or_create(
                    performance=obj,
                    price_category=category,
                    defaults={'price': category.base_price}
                )


@admin.register(Show)
class ShowAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'venue', 'duration_minutes', 'is_active', 'upcoming_performances']
    list_filter = ['venue', 'category', 'is_active']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [PerformanceInline]
    readonly_fields = ['created_at', 'updated_at']

    def get_fields(self, request, obj=None):
        if request.user.is_superuser:
            return super().get_fields(request, obj)
        else:
            return ['name', 'slug', 'category', 'duration_minutes', 'description', 'poster', 'is_active']

    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return self.readonly_fields
        else:
            return self.readonly_fields + ['venue']

    def save_model(self, request, obj, form, change):
        if not obj.venue_id:
            from venues.models import Venue
            default_venue = Venue.objects.first()
            if default_venue:
                obj.venue = default_venue

        super().save_model(request, obj, form, change)

    def upcoming_performances(self, obj):
        count = obj.performances.filter(
            datetime__gte=timezone.now(),
            status='on_sale'
        ).count()
        return format_html('<span class="badge">{}</span>', count)
    upcoming_performances.short_description = 'Suất sắp diễn'

    actions = ['create_week_performances', 'activate_shows', 'deactivate_shows']

    def create_week_performances(self, request, queryset):
        """Quick action to create performances for next 7 days"""
        for show in queryset:
            start_date = timezone.now().replace(hour=19, minute=0, second=0, microsecond=0)

            for day in range(7):
                performance_date = start_date + timedelta(days=day)

                # Create 2 performances per day (19:00 and 21:00)
                for hour in [19, 21]:
                    perf_datetime = performance_date.replace(hour=hour)

                    perf = Performance.objects.create(
                        show=show,
                        datetime=perf_datetime,
                        status='on_sale'
                    )

                    # Auto create prices
                    for category in PriceCategory.objects.all():
                        PerformancePrice.objects.create(
                            performance=perf,
                            price_category=category,
                            price=category.base_price
                        )

        self.message_user(request, f"Đã tạo suất diễn cho {queryset.count()} show trong 7 ngày tới")
    create_week_performances.short_description = "Tạo suất diễn 7 ngày tới"

    def activate_shows(self, request, queryset):
        queryset.update(is_active=True)
    activate_shows.short_description = "Kích hoạt show"

    def deactivate_shows(self, request, queryset):
        queryset.update(is_active=False)
    deactivate_shows.short_description = "Tắt show"


# Simplified Performance Admin
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
