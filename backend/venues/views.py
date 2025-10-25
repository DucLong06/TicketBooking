from django.db.models import Q, Count
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from django.utils import timezone
from shows.models import Show, Performance
from shows.serializers import ShowListSerializer, ShowDetailSerializer, PerformanceSerializer

from . models import ContactInfo, Row
from .serializers import ContactInfoSerializer


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


class ContactInfoViewSet(viewsets.ReadOnlyModelViewSet):
    """API for Contact Information - Read only"""
    queryset = ContactInfo.objects.all()
    serializer_class = ContactInfoSerializer

    def list(self, request, *args, **kwargs):
        """Always return the singleton instance"""
        contact = ContactInfo.get_instance()
        serializer = self.get_serializer(contact)
        return Response(serializer.data)


@api_view(['PATCH'])
def toggle_row_orphan_rule(request, row_id):
    """Toggle orphan seat rule for a specific row"""
    row = get_object_or_404(Row, id=row_id)
    enabled = request.data.get('enabled')

    if enabled is not None:
        row.orphan_seat_rule_enabled = enabled
    else:
        row.orphan_seat_rule_enabled = not row.orphan_seat_rule_enabled

    row.save()

    return Response({
        'row_id': row.id,
        'row_label': row.label,
        'orphan_seat_rule_enabled': row.orphan_seat_rule_enabled
    })


@api_view(['PATCH'])
def toggle_venue_orphan_rule(request, venue_id):
    """Toggle orphan seat rule for all rows in a venue"""
    from .models import Venue
    venue = get_object_or_404(Venue, id=venue_id)
    enabled = request.data.get('enabled', True)

    # Update all rows in venue
    Row.objects.filter(
        section__venue=venue
    ).update(orphan_seat_rule_enabled=enabled)

    return Response({
        'venue_id': venue.id,
        'orphan_seat_rule_enabled': enabled,
        'updated_rows': Row.objects.filter(section__venue=venue).count()
    })
