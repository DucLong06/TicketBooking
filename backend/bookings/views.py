from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from .email_service import send_booking_confirmation
from logzero import logger
from shows.models import Performance, PerformancePrice
from venues.models import Seat
from .serializers import (
    BookingDetailSerializer,
    BookingCreateSerializer,
    ReserveSeatSerializer,
)
from .models import Booking, SeatReservation
from django.conf import settings
from django.db.models import Prefetch
from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db import transaction
from datetime import timezone as dt_timezone 
from datetime import timedelta


def get_performance_seat_map(performance):
    """Get complete seat map for a performance"""
    venue = performance.show.venue

    # Get all seats
    seats = Seat.objects.filter(
        row__section__venue=venue,
        status='active'
    ).select_related(
        'row',
        'row__section',
        'row__price_category',
        'price_category'
    ).prefetch_related(
        Prefetch(
            'reservations',
            queryset=SeatReservation.objects.filter(
                performance=performance,
                status__in=['reserved', 'sold', 'blocked']
            ),
            to_attr='active_reservations'
        )
    )

    # Get reservations
    reservations = SeatReservation.objects.filter(
        performance=performance,
        status__in=['reserved', 'sold', 'blocked']
    ).values('seat_id', 'status')
    reservation_map = {r['seat_id']: r['status'] for r in reservations}

    # Get performance prices
    performance_prices = PerformancePrice.objects.filter(
        performance=performance
    ).values('price_category_id', 'price')
    price_map = {pp['price_category_id']: pp['price'] for pp in performance_prices}

    utc_plus_7 = dt_timezone(timedelta(hours=7))
    datetime_in_utc7 = performance.datetime.astimezone(utc_plus_7)

    # Build seat map data
    seat_map_data = {
        'venue': {
            'name': venue.name,
            'address': venue.address,
            'phone': venue.phone,
            'hotline': venue.hotline_display,

            'layout_image_url': venue.layout_image.url if venue.layout_image else None,
            'checkin_minutes_before': venue.checkin_minutes_before,
            'width': 800,
            'height': 900
        },
        'show': {
            'name': performance.show.name,
            'description': performance.show.description,
            'duration_minutes': performance.show.duration_minutes,
        },
        'performance': {
            'id': performance.id,
            'datetime': datetime_in_utc7.isoformat(),
            'date': datetime_in_utc7.strftime('%d/%m/%Y'),
            'time': datetime_in_utc7.strftime('%H:%M'),
            'day_of_week': ['Thứ Hai', 'Thứ Ba', 'Thứ Tư', 'Thứ Năm', 'Thứ Sáu', 'Thứ Bảy', 'Chủ Nhật'][datetime_in_utc7.weekday()],
        },
        'sections': [],
        'seats': [],
        'numbering_info': {}
    }

    sections_dict = {}
    rows_dict = {}

    for seat in seats:
        section = seat.row.section
        row = seat.row

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

        # Track row info
        if row.id not in rows_dict:
            rows_dict[row.id] = {
                'row': row,
                'seats': []
            }
        rows_dict[row.id]['seats'].append(seat)

        # Determine seat status
        seat_status = reservation_map.get(seat.id, 'available')

        # Get price per seat
        effective_pc = seat.effective_price_category
        price_category_id = effective_pc.id if effective_pc else None

        seat_price = price_map.get(
            price_category_id,
            effective_pc.base_price if effective_pc else 0
        )

        # Safe number conversion
        try:
            seat_number = int(seat.number)
            remainder = seat_number % 2
            is_odd_number = remainder == 1
            is_even_number = remainder == 0
            seat_side = 'left' if is_odd_number else 'right'
        except (ValueError, TypeError):
            seat_number = seat.display_label
            is_odd_number = False
            is_even_number = False
            seat_side = 'center'

        # Build seat data
        seat_data = {
            'id': seat.id,
            'section_id': section.code,
            'section_name': section.name,
            'row': seat.row.label,
            'row_position_y': seat.row.position_y,
            'row_spacing_after': seat.row.spacing_after,
            'number': seat.number,
            'display_number': seat.display_label,
            'full_label': seat.full_display_label,
            'position_x': seat.position_x,
            'position_y': seat.position_y,
            'spacing_after': seat.spacing_after,
            'status': seat_status,

            # Price & Category
            'price': float(seat_price),
            'price_category': effective_pc.code if effective_pc else 'standard',
            'price_category_color': effective_pc.color if effective_pc else '#10B981',
            'effective_price_category_name': effective_pc.name if effective_pc else 'Standard',


            'seat_image_url': seat.seat_image.url if seat.seat_image else None,

            'is_accessible': seat.is_accessible,
            'numbering_style': safe_getattr(seat.row, 'numbering_style', 'left_to_right'),
            'is_odd': is_odd_number,
            'is_even': is_even_number,
            'side': seat_side
        }

        seat_map_data['seats'].append(seat_data)

    # Add numbering info per row
    for row_id, row_data in rows_dict.items():
        row = row_data['row']
        row_key = f"{row.section.code}-{row.label}"

        seat_map_data['numbering_info'][row_key] = {
            'numbering_style': safe_getattr(row, 'numbering_style', 'left_to_right'),
            'center_x': safe_getattr(row, 'center_x', 400),
            'aisle_width': safe_getattr(row, 'aisle_width', 60),
            'has_center_aisle': safe_getattr(row, 'has_center_aisle', True),
            'gaps': safe_getattr(row, 'gaps', []),
            'total_seats': row.seat_count,
            'actual_seats': len(row_data['seats']),
            'actual_seat_numbers': [s.number for s in row.seats.all()],
        }

    # Add price categories
    from venues.models import PriceCategory
    all_categories = PriceCategory.objects.all()
    sorted_categories = all_categories.order_by('base_price')
    seat_map_data['price_categories'] = {}
    for pc in sorted_categories:
        performance_price = price_map.get(pc.id, pc.base_price)
        seat_map_data['price_categories'][pc.code] = {
            'name': pc.name,
            'price': float(performance_price),
            'color': pc.color
        }

    return seat_map_data


def safe_getattr(obj, attr_name, default_value):
    """Safely get attribute with fallback"""
    try:
        return getattr(obj, attr_name, default_value)
    except (AttributeError, TypeError):
        return default_value


@api_view(['GET'])
def performance_seat_map(request, performance_id):
    """API endpoint to get seat map"""
    performance = get_object_or_404(Performance, id=performance_id)
    seat_map_data = get_performance_seat_map(performance)
    return Response(seat_map_data)


@api_view(['POST'])
@csrf_exempt
def reserve_seats(request):
    """Reserve seats temporarily"""
    serializer = ReserveSeatSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    performance_id = serializer.validated_data['performance_id']
    seat_ids = serializer.validated_data['seat_ids']
    session_id = serializer.validated_data['session_id']

    performance = Performance.objects.get(id=performance_id)

    with transaction.atomic():
        # Release expired reservations
        expired_reservations = SeatReservation.objects.filter(
            performance=performance,
            status='reserved',
            expires_at__lt=timezone.now()
        )
        expired_reservations.update(status='available', session_id='', expires_at=None)

        # Check availability
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
        timeout_minutes = getattr(settings, 'SEAT_RESERVATION_TIMEOUT_MINUTES', 5)
        existing_reservation = SeatReservation.objects.filter(
            performance=performance,
            session_id=session_id,
            status='reserved',
            expires_at__isnull=False
        ).first()

        if existing_reservation and existing_reservation.expires_at:
            expires_at = existing_reservation.expires_at
        else:
            expires_at = timezone.now() + timedelta(minutes=timeout_minutes)

        for seat_id in seat_ids:
            seat = Seat.objects.select_related(
                'row',
                'row__price_category',
                'price_category'
            ).get(id=seat_id)

            # ===== GET PRICE FROM SEAT'S PRICE_CATEGORY =====
            effective_pc = seat.effective_price_category
            price_category_id = effective_pc.id if effective_pc else None
            seat_price = price_map.get(
                price_category_id,
                effective_pc.base_price if effective_pc else 0
            )

            reservation, created = SeatReservation.objects.update_or_create(
                performance=performance,
                seat_id=seat_id,
                defaults={
                    'status': 'reserved',
                    'session_id': session_id,
                    'price': seat_price,  # ← Giá theo price_category của ghế
                    'expires_at': expires_at
                }
            )

            reserved_seats.append({
                'id': seat.id,
                'row': seat.row.label,
                'number': seat.display_label,      # ← Display number
                'full_label': seat.full_display_label,
                'section_name': seat.row.section.name,
                'price': float(seat_price)
            })

    return Response({
        'seats': reserved_seats,
        'expires_at': expires_at.isoformat(),
        'timeout_seconds': timeout_minutes * 60
    })


@api_view(['POST'])
@csrf_exempt
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


@method_decorator(csrf_exempt, name='dispatch')
class BookingViewSet(viewsets.ModelViewSet):
    """API for Bookings"""
    queryset = Booking.objects.all()
    serializer_class = BookingDetailSerializer
    lookup_field = 'booking_code'

    def get_serializer_class(self):
        if self.action == 'create':
            return BookingCreateSerializer
        return BookingDetailSerializer

    def create(self, request, *args, **kwargs):
        """Create a new booking"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        with transaction.atomic():
            booking = serializer.save()

        # Return booking details
        detail_serializer = BookingDetailSerializer(booking)
        response_data = detail_serializer.data

        response_data['expires_at'] = booking.expires_at.isoformat()
        response_data['timeout_seconds'] = int((booking.expires_at - timezone.now()).total_seconds())

        return Response(
            response_data,
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

    @action(detail=True, methods=['post'], url_path='resend-email')
    def resend_email(self, request, booking_code=None):
        """Resend booking confirmation email"""
        booking = self.get_object()

        if booking.status not in ['paid', 'confirmed']:
            return Response(
                {'error': 'Chỉ có thể gửi lại email cho đơn đã thanh toán'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Send email
            success = send_booking_confirmation(booking)

            if success:
                return Response({
                    'success': True,
                    'message': 'Email đã được gửi lại thành công!'
                })
            else:
                return Response(
                    {'error': 'Không thể gửi email. Vui lòng thử lại sau.'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        except Exception as e:
            logger.error(f"Error resending email for booking {booking_code}: {e}")
            return Response(
                {'error': 'Lỗi hệ thống. Vui lòng thử lại sau.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
