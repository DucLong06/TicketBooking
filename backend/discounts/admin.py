from django.contrib import admin
from .models import Discount, DiscountUsage


class DiscountUsageInline(admin.TabularInline):
    model = DiscountUsage
    extra = 0
    readonly_fields = ('booking', 'used_at', 'status')
    can_delete = False


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount_type', 'value', 'min_ticket_quantity', 'max_usage', 'usage_count',
                    'valid_from', 'valid_to', 'is_active')
    list_filter = ('discount_type', 'is_active', 'all_users')
    search_fields = ('code', 'allowed_users')
    inlines = [DiscountUsageInline]
    fieldsets = (
        ('Thông tin cơ bản', {
            'fields': ('code', 'discount_type', 'value', 'is_active')
        }),
        ('Điều kiện áp dụng', {
            'fields': ('min_ticket_quantity', 'max_usage', 'valid_from', 'valid_to')
        }),
        ('Phân quyền người dùng', {
            'fields': ('all_users', 'allowed_users')
        }),
        ('Thống kê', {
            'fields': ('usage_count',),
            'classes': ('collapse',)
        })
    )
    readonly_fields = ('usage_count',)
