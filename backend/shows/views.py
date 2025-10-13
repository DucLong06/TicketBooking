from django.db.models import Q, Count
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from .models import Show, Performance, Poster
from .serializers import (
    ShowListSerializer,
    ShowDetailSerializer,
    PerformanceSerializer,
    PosterSerializer
)


class ShowViewSet(viewsets.ReadOnlyModelViewSet):
    """API for Shows"""
    queryset = Show.objects.filter(is_active=True)

    def get_serializer_class(self):
        if self.action == 'list':
            return ShowListSerializer
        return ShowDetailSerializer

    @action(detail=True, methods=['get'])
    def performances(self, request, pk=None):
        """Get performances for a show"""
        show = self.get_object()
        performances = show.performances.filter(
            datetime__gte=timezone.now(),
            status='on_sale'
        ).order_by('datetime')

        serializer = PerformanceSerializer(performances, many=True)
        return Response(serializer.data)


class PerformanceViewSet(viewsets.ReadOnlyModelViewSet):
    """API for Performances"""
    serializer_class = PerformanceSerializer

    def get_queryset(self):
        return Performance.objects.annotate(
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
    queryset = Poster.objects.filter(is_active=True).select_related('show')
    serializer_class = PosterSerializer

    def get_queryset(self):
        return super().get_queryset().order_by('order', '-created_at')
