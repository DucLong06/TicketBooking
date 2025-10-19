from django.db.models import Q, Count, Prefetch
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from django.core.cache import cache
from .models import Show, Performance, Poster, PerformancePrice
from .serializers import (
    ShowListSerializer,
    ShowDetailSerializer,
    PerformanceSerializer,
    PosterSerializer
)

from venues.models import Section, Row
from django.db.models import Prefetch
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from .models import Show, Performance, PerformancePrice
from .serializers import (
    ShowListSerializer,
    ShowDetailSerializer,
    PerformanceSerializer,
)


class ShowViewSet(viewsets.ReadOnlyModelViewSet):
    def get_serializer_class(self):
        if self.action == 'list':
            return ShowListSerializer
        return ShowDetailSerializer

    def get_queryset(self):
        queryset = Show.objects.filter(is_active=True)

        if self.action == 'retrieve':
            queryset = queryset.select_related(
                'venue',
                'venue__layout'
            ).prefetch_related(
                Prefetch(
                    'performances',
                    queryset=Performance.objects.filter(
                        datetime__gte=timezone.now(),
                        status='on_sale'
                    ).prefetch_related(
                        Prefetch(
                            'prices',
                            queryset=PerformancePrice.objects.select_related(
                                'price_category'
                            )
                        )
                    ).order_by('datetime')
                ),
                Prefetch(
                    'venue__sections',
                    queryset=Section.objects.prefetch_related(
                        Prefetch(
                            'rows',
                            queryset=Row.objects.prefetch_related(
                                'price_category'
                            )
                        )
                    ).order_by('order')
                )
            )

        return queryset

    def list(self, request, *args, **kwargs):
        cache_key = 'shows_list'
        cached_data = cache.get(cache_key)
        if cached_data:
            return Response(cached_data)

        response = super().list(request, *args, **kwargs)
        cache.set(cache_key, response.data, 3600)  # Cache 1 giờ
        return response

    def retrieve(self, request, *args, **kwargs):
        show_id = kwargs.get('pk')
        cache_key = f'show_detail_{show_id}'
        cached_data = cache.get(cache_key)
        if cached_data:
            return Response(cached_data)

        response = super().retrieve(request, *args, **kwargs)
        cache.set(cache_key, response.data, 3600)  # Cache 1 giờ
        return response

    @action(detail=True, methods=['get'])
    def performances(self, request, pk=None):
        """Get performances for a show"""
        show = self.get_object()
        performances = show.performances.filter(
            datetime__gte=timezone.now(),
            status='on_sale'
        ).prefetch_related(
            Prefetch(
                'prices',
                queryset=PerformancePrice.objects.select_related('price_category')
            )
        ).order_by('datetime')

        serializer = PerformanceSerializer(performances, many=True)
        return Response(serializer.data)


class PerformanceViewSet(viewsets.ReadOnlyModelViewSet):
    """API for Performances - OPTIMIZED"""
    serializer_class = PerformanceSerializer

    def get_queryset(self):
        """✅ Optimized queryset with prefetch"""
        return Performance.objects.select_related(
            'show',
            'show__venue'
        ).prefetch_related(
            Prefetch(
                'prices',
                queryset=PerformancePrice.objects.select_related('price_category')
            )
        ).annotate(
            available_seats=Count('show__venue__sections__rows__seats') - Count(
                'seat_reservations',
                filter=Q(seat_reservations__status__in=['reserved', 'sold'])
            )
        )

    @action(detail=True, methods=['get'])
    def seat_map(self, request, pk=None):
        """Get seat map for a performance"""
        from bookings.views import get_performance_seat_map
        performance = self.get_object()
        seat_map_data = get_performance_seat_map(performance)
        return Response(seat_map_data)


class PosterViewSet(viewsets.ReadOnlyModelViewSet):
    """API for Homepage Posters/Banners"""
    serializer_class = PosterSerializer

    def list(self, request, *args, **kwargs):
        cache_key = 'posters_list'
        cached_data = cache.get(cache_key)
        if cached_data:
            return Response(cached_data)

        response = super().list(request, *args, **kwargs)
        cache.set(cache_key, response.data, 3600 * 6)
        return response

    def get_queryset(self):
        return Poster.objects.filter(
            is_active=True
        ).select_related(
            'show',
            'show__venue'
        ).order_by('order', '-created_at')
