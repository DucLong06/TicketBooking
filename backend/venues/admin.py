from django.contrib import admin
from .models import Venue, Section, PriceCategory, Row, Seat


@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    list_display = ['name', 'address', 'phone', 'email', 'created_at']
    search_fields = ['name', 'address']
    readonly_fields = ['created_at', 'updated_at']


class RowInline(admin.TabularInline):
    model = Row
    extra = 1


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ['name', 'venue', 'code', 'order']
    list_filter = ['venue']
    search_fields = ['name', 'code']
    inlines = [RowInline]
    ordering = ['venue', 'order']


@admin.register(PriceCategory)
class PriceCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'base_price', 'color']
    search_fields = ['name', 'code']


class SeatInline(admin.TabularInline):
    model = Seat
    extra = 0
    fields = ['number', 'position_x', 'position_y', 'status', 'is_accessible']


@admin.register(Row)
class RowAdmin(admin.ModelAdmin):
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
