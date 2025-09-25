from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db import transaction
from datetime import timedelta
from django.conf import settings
from .models import Booking, SeatReservation
from .serializers import (
    BookingDetailSerializer,
    CreateBookingSerializer,
    ReserveSeatSerializer,
    SeatMapSerializer
)
from venues.models import Seat
from shows.models import Performance, PerformancePrice
from .email_service import send_booking_confirmation


def get_performance_seat_map(performance):
    """Get complete seat map for a performance"""
    venue = performance.show.venue

    # Get all seats in venue
    seats = Seat.objects.filter(
        row__section__venue=venue,
        status='active'
    ).select_related('row', 'row__section', 'row__price_category')

    # Get existing reservations
    reservations = SeatReservation.objects.filter(
        performance=performance,
        status__in=['reserved', 'sold', 'blocked']
    ).values('seat_id', 'status')

    reservation_map = {r['seat_id']: r['status'] for r in reservations}

    # Get prices for this performance
    performance_prices = PerformancePrice.objects.filter(
        performance=performance
    ).values('price_category_id', 'price')

    price_map = {pp['price_category_id']: pp['price'] for pp in performance_prices}

    # Build seat map data
    seat_map_data = {
        'venue': {
            'name': venue.name,
            'width': 800,
            'height': 900
        },
        'sections': [],
        'seats': []
    }

    sections_dict = {}

    for seat in seats:
        section = seat.row.section

        # Add section if not exists
        if section.id not in sections_dict:
            sections_dict[section.id] = {
                'id': section.code,
                'name': section.name,
                'position': {
                    'x': section.position_x,
                    'y': section.position_y
                }
            }
            seat_map_data['sections'].append(sections_dict[section.id])

        # Determine seat status
        if seat.id in reservation_map:
            seat_status = reservation_map[seat.id]
        else:
            seat_status = 'available'

        # Get price for this seat
        price_category_id = seat.row.price_category_id
        price = price_map.get(price_category_id, seat.row.price_category.base_price)

        # Add seat data
        seat_data = {
            'id': seat.id,
            'section_id': section.code,
            'section_name': section.name,
            'row': seat.row.label,
            'number': seat.number,
            'x': seat.position_x,
            'y': seat.position_y,
            'status': seat_status,
            'price': float(price),
            'price_category': seat.row.price_category.code if seat.row.price_category else 'standard',
            'is_accessible': seat.is_accessible
        }

        seat_map_data['seats'].append(seat_data)

    # Add price categories
    seat_map_data['price_categories'] = {
        pc.code: {
            'name': pc.name,
            'price': float(price_map.get(pc.id, pc.base_price)),
            'color': pc.color
        }
        for pc in venue.sections.first().rows.first().price_category.__class__.objects.all()
    }

    return seat_map_data


@api_view(['GET'])
def performance_seat_map(request, performance_id):
    """API endpoint to get seat map"""
    performance = get_object_or_404(Performance, id=performance_id)
    seat_map_data = get_performance_seat_map(performance)
    return Response(seat_map_data)


@api_view(['POST'])
def reserve_seats(request):
    """Reserve seats temporarily"""
    serializer = ReserveSeatSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    performance_id = serializer.validated_data['performance_id']
    seat_ids = serializer.validated_data['seat_ids']
    session_id = serializer.validated_data['session_id']

    performance = Performance.objects.get(id=performance_id)

    with transaction.atomic():
        # Release any expired reservations first
        expired_reservations = SeatReservation.objects.filter(
            performance=performance,
            status='reserved',
            expires_at__lt=timezone.now()
        )
        expired_reservations.update(status='available', session_id='', expires_at=None)

        # Check if seats are available
        existing_reservations = SeatReservation.objects.filter(
            performance=performance,
            seat_id__in=seat_ids,
            status__in=['reserved', 'sold']
        ).exclude(session_id=session_id)

        if existing_reservations.exists():
            return Response(
                {'error': 'Một số ghế đã được đặt'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Get performance prices
        performance_prices = PerformancePrice.objects.filter(
            performance=performance
        ).values('price_category_id', 'price')

        price_map = {pp['price_category_id']: pp['price'] for pp in performance_prices}

        # Reserve seats
        reserved_seats = []
        timeout_minutes = getattr(settings, 'BOOKING_TIMEOUT_MINUTES', 10)
        expires_at = timezone.now() + timedelta(minutes=timeout_minutes)

        for seat_id in seat_ids:
            seat = Seat.objects.get(id=seat_id)
            price_category_id = seat.row.price_category_id
            price = price_map.get(price_category_id, seat.row.price_category.base_price)

            reservation, created = SeatReservation.objects.update_or_create(
                performance=performance,
                seat_id=seat_id,
                defaults={
                    'status': 'reserved',
                    'session_id': session_id,
                    'price': price,
                    'expires_at': expires_at
                }
            )

            reserved_seats.append({
                'id': seat.id,
                'row': seat.row.label,
                'number': seat.number,
                'section_name': seat.row.section.name,
                'price': float(price)
            })

    return Response({
        'seats': reserved_seats,
        'expires_at': expires_at.isoformat(),
        'timeout_seconds': timeout_minutes * 60
    })


@api_view(['POST'])
def release_seats(request):
    """Release reserved seats"""
    session_id = request.data.get('session_id')
    seat_ids = request.data.get('seat_ids', [])

    if not session_id:
        return Response(
            {'error': 'session_id is required'},
            status=status.HTTP_400_BAD_REQUEST
        )

    reservations = SeatReservation.objects.filter(
        session_id=session_id,
        seat_id__in=seat_ids,
        status='reserved'
    )

    count = reservations.update(
        status='available',
        session_id='',
        expires_at=None
    )

    return Response({'released': count})


class BookingViewSet(viewsets.ModelViewSet):
    """API for Bookings"""
    queryset = Booking.objects.all()
    serializer_class = BookingDetailSerializer
    lookup_field = 'booking_code'

    def get_serializer_class(self):
        if self.action == 'create':
            return CreateBookingSerializer
        return BookingDetailSerializer

    def create(self, request, *args, **kwargs):
        """Create a new booking"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        with transaction.atomic():
            booking = serializer.save()

        # Return booking details
        detail_serializer = BookingDetailSerializer(booking)
        return Response(
            detail_serializer.data,
            status=status.HTTP_201_CREATED
        )

    @action(detail=True, methods=['post'])
    def cancel(self, request, booking_code=None):
        """Cancel a booking"""
        booking = self.get_object()

        if booking.status != 'pending':
            return Response(
                {'error': 'Chỉ có thể hủy đơn đang chờ thanh toán'},
                status=status.HTTP_400_BAD_REQUEST
            )

        with transaction.atomic():
            booking.status = 'cancelled'
            booking.save()

            # Release seats
            booking.seat_reservations.update(
                status='available',
                session_id='',
                expires_at=None
            )

        return Response({'status': 'cancelled'})
