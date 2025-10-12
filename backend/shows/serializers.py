from rest_framework import serializers
from django.utils import timezone
from .models import Show, Performance, PerformancePrice, Poster
from venues.serializers import VenueSerializer


class ShowListSerializer(serializers.ModelSerializer):
    venue_name = serializers.CharField(source='venue.name', read_only=True)
    min_price = serializers.SerializerMethodField()
    max_price = serializers.SerializerMethodField()

    service_fee_per_ticket = serializers.DecimalField(
        max_digits=10,
        decimal_places=0,
        read_only=True
    )

    class Meta:
        model = Show
        fields = [
            'id', 'name', 'slug', 'category', 'duration_minutes',
            'description', 'poster', 'venue_name', 'min_price', 'max_price', 'service_fee_per_ticket'
        ]

    def get_min_price(self, obj):
        prices = PerformancePrice.objects.filter(
            performance__show=obj,
            performance__datetime__gte=timezone.now()
        ).values_list('price', flat=True)
        return min(prices) if prices else 0

    def get_max_price(self, obj):
        prices = PerformancePrice.objects.filter(
            performance__show=obj,
            performance__datetime__gte=timezone.now()
        ).values_list('price', flat=True)
        return max(prices) if prices else 0


class PerformancePriceSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='price_category.name', read_only=True)
    category_code = serializers.CharField(source='price_category.code', read_only=True)

    class Meta:
        model = PerformancePrice
        fields = ['id', 'price_category', 'category_name', 'category_code', 'price']


class PerformanceSerializer(serializers.ModelSerializer):
    prices = PerformancePriceSerializer(many=True, read_only=True)
    available_seats = serializers.IntegerField(source='available_seats_count', read_only=True)

    class Meta:
        model = Performance
        fields = [
            'id', 'datetime', 'status', 'available_seats',
            'prices', 'notes'
        ]


class ShowDetailSerializer(serializers.ModelSerializer):
    venue = VenueSerializer(read_only=True)
    performances = serializers.SerializerMethodField()
    service_fee_per_ticket = serializers.DecimalField(
        max_digits=10,
        decimal_places=0,
        read_only=True
    )

    class Meta:
        model = Show
        fields = [
            'id', 'name', 'slug', 'category', 'duration_minutes',
            'description', 'poster', 'venue', 'performances', 'service_fee_per_ticket'
        ]

    def get_performances(self, obj):
        # Only get future performances
        performances = obj.performances.filter(
            datetime__gte=timezone.now(),
            status='on_sale'
        ).order_by('datetime')
        return PerformanceSerializer(performances, many=True).data


class PosterSerializer(serializers.ModelSerializer):
    show_id = serializers.IntegerField(source='show.id', read_only=True)
    show_name = serializers.CharField(source='show.name', read_only=True)
    show_slug = serializers.CharField(source='show.slug', read_only=True)

    class Meta:
        model = Poster
        fields = [
            'id', 'title', 'image',
            'show_id', 'show_name', 'show_slug',
            'order'
        ]
