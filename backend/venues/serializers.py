from .models import Venue, Section, Row, Seat, PriceCategory, VenueLayout, ContactInfo
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

    numbering_style = serializers.CharField(source='row.numbering_style', read_only=True)
    row_position_y = serializers.IntegerField(source='row.position_y', read_only=True)
    row_spacing_after = serializers.IntegerField(default=0, read_only=True)

    # Display fields
    display_number = serializers.CharField(source='display_label', read_only=True)
    full_display_label = serializers.CharField(read_only=True)

    # Price category fields
    effective_price_category_code = serializers.CharField(
        source='effective_price_category.code',
        read_only=True
    )
    effective_price_category_name = serializers.CharField(
        source='effective_price_category.name',
        read_only=True
    )
    effective_price_category_color = serializers.CharField(
        source='effective_price_category.color',
        read_only=True
    )

    seat_image_url = serializers.SerializerMethodField()

    class Meta:
        model = Seat
        fields = [
            'id',
            'number',
            'display_number',
            'full_display_label',
            'row_label',
            'section_name',
            'section_id',
            'numbering_style',
            'row_position_y',
            'row_spacing_after',  # THÊM field này
            'position_x',
            'position_y',
            'spacing_after',
            'status',
            'is_accessible',
            'effective_price_category_code',
            'effective_price_category_name',
            'effective_price_category_color',
            'seat_image_url'
        ]

    def get_seat_image_url(self, obj):
        if obj.seat_image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.seat_image.url)
            return obj.seat_image.url
        return None


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
            'description', 'rules', 'layout', 'total_seats', 'sections'
        ]

    def get_total_seats(self, obj):
        return Seat.objects.filter(
            row__section__venue=obj,
            status='active'
        ).count()


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
        return obj.sections.count() * 200  # Rough estimate


class ContactInfoSerializer(serializers.ModelSerializer):
    hotline_display = serializers.ReadOnlyField()

    class Meta:
        model = ContactInfo
        fields = [
            'id', 'name', 'hotline', 'hotline_display',
            'support_email', 'facebook_url', 'tiktok_url',
            'instagram_url', 'website_url', 'logo_url',
            'copyright_text'
        ]
