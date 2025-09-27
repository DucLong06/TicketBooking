from .models import Venue, Section, Row, Seat, PriceCategory, VenueLayout
from rest_framework import serializers
from django.db import models

class VenueLayoutSerializer(serializers.ModelSerializer):
    total_seats = serializers.ReadOnlyField()

    class Meta:
        model = VenueLayout
        fields = [
            'id', 'name', 'venue_type', 'description',
            'config', 'is_template', 'total_seats'
        ]


class PriceCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PriceCategory
        fields = ['id', 'name', 'code', 'base_price', 'color']


class SeatSerializer(serializers.ModelSerializer):
    row_label = serializers.CharField(source='row.label', read_only=True)
    section_name = serializers.CharField(source='row.section.name', read_only=True)
    section_id = serializers.CharField(source='row.section.code', read_only=True)
    price_category = serializers.CharField(source='row.price_category.code', read_only=True)
    price_category_color = serializers.CharField(source='row.price_category.color', read_only=True)

    class Meta:
        model = Seat
        fields = [
            'id', 'number', 'row_label', 'section_name', 'section_id',
            'position_x', 'position_y', 'status', 'is_accessible',
            'price_category', 'price_category_color'
        ]


class RowSerializer(serializers.ModelSerializer):
    seats = SeatSerializer(many=True, read_only=True)
    price_category = PriceCategorySerializer(read_only=True)
    actual_seat_count = serializers.SerializerMethodField()

    class Meta:
        model = Row
        fields = [
            'id', 'label', 'seat_count', 'actual_seat_count',
            'position_y', 'price_category', 'seats'
        ]

    def get_actual_seat_count(self, obj):
        return obj.seats.count()


class SectionSerializer(serializers.ModelSerializer):
    rows = RowSerializer(many=True, read_only=True)
    seat_count = serializers.SerializerMethodField()

    class Meta:
        model = Section
        fields = [
            'id', 'name', 'code', 'position_x', 'position_y',
            'order', 'seat_count', 'rows'
        ]

    def get_seat_count(self, obj):
        return sum(row.seats.count() for row in obj.rows.all())


class VenueSerializer(serializers.ModelSerializer):
    sections = SectionSerializer(many=True, read_only=True)
    layout = VenueLayoutSerializer(read_only=True)
    total_seats = serializers.SerializerMethodField()

    class Meta:
        model = Venue
        fields = [
            'id', 'name', 'venue_type', 'address', 'phone', 'email',
            'description', 'layout', 'total_seats', 'sections'
        ]

    def get_total_seats(self, obj):
        return sum(
            section.rows.aggregate(
                total=models.Sum('seats__id')
            )['total'] or 0
            for section in obj.sections.all()
        )


class VenueListSerializer(serializers.ModelSerializer):
    """Serializer đơn giản cho danh sách venues"""
    layout_name = serializers.CharField(source='layout.name', read_only=True)
    total_seats = serializers.SerializerMethodField()

    class Meta:
        model = Venue
        fields = [
            'id', 'name', 'venue_type', 'address',
            'layout_name', 'total_seats'
        ]

    def get_total_seats(self, obj):
        # Simplified calculation for list view
        return obj.sections.count() * 200  # Rough estimate
