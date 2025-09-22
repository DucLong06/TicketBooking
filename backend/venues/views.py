from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from .models import Show, Performance
from .serializers import ShowListSerializer, ShowDetailSerializer, PerformanceSerializer


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
    queryset = Performance.objects.filter(
        datetime__gte=timezone.now(),
        status='on_sale'
    )
    serializer_class = PerformanceSerializer

    @action(detail=True, methods=['get'])
    def seat_map(self, request, pk=None):
        """Get seat map for a performance"""
        from bookings.views import get_performance_seat_map
        performance = self.get_object()
        seat_map_data = get_performance_seat_map(performance)
        return Response(seat_map_data)
