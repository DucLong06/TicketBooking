from .models import Venue, Section, Row, Seat, PriceCategory
from rest_framework import serializers


class PriceCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PriceCategory
        fields = ['id', 'name', 'code', 'base_price', 'color']


class SeatSerializer(serializers.ModelSerializer):
    row_label = serializers.CharField(source='row.label', read_only=True)
    section_name = serializers.CharField(source='row.section.name', read_only=True)
    section_id = serializers.CharField(source='row.section.code', read_only=True)
    price_category = serializers.CharField(source='row.price_category.code', read_only=True)

    class Meta:
        model = Seat
        fields = [
            'id', 'number', 'row_label', 'section_name', 'section_id',
            'position_x', 'position_y', 'status', 'is_accessible',
            'price_category'
        ]


class RowSerializer(serializers.ModelSerializer):
    seats = SeatSerializer(many=True, read_only=True)
    price_category = PriceCategorySerializer(read_only=True)

    class Meta:
        model = Row
        fields = ['id', 'label', 'seat_count', 'position_y', 'price_category', 'seats']


class SectionSerializer(serializers.ModelSerializer):
    rows = RowSerializer(many=True, read_only=True)

    class Meta:
        model = Section
        fields = ['id', 'name', 'code', 'position_x', 'position_y', 'order', 'rows']


class VenueSerializer(serializers.ModelSerializer):
    sections = SectionSerializer(many=True, read_only=True)

    class Meta:
        model = Venue
        fields = ['id', 'name', 'address', 'phone', 'email', 'description', 'sections']
