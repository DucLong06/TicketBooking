from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from .email_service import send_booking_confirmation
from logzero import logger
from shows.models import Performance, PerformancePrice
from venues.models import Row, Seat
from .serializers import (
    BookingDetailSerializer,
    BookingCreateSerializer,
    ReserveSeatSerializer,
)
from .models import Booking, SeatReservation, BookingHistory
from django.conf import settings
from django.db.models import Prefetch, Q
from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db import transaction
from datetime import timezone as dt_timezone
from datetime import timedelta


def validate_orphan_seats(selected_seat_ids, performance):

    seats = Seat.objects.filter(
        id__in=selected_seat_ids
    ).select_related('row').only('id', 'row_id', 'number', 'display_number')

    # Group seats by row
    rows_to_check = {}
    for seat in seats:
        if seat.row_id not in rows_to_check:
            rows_to_check[seat.row_id] = {
                'row': seat.row,
                'seat_ids': []
            }
        rows_to_check[seat.row_id]['seat_ids'].append(seat.id)

    row_ids_with_rule = [
        row_id for row_id, data in rows_to_check.items()
        if data['row'].orphan_seat_rule_enabled
    ]

    if not row_ids_with_rule:
        return (True, None)

    all_seats_map = {}
    all_seats = Seat.objects.filter(
        row_id__in=row_ids_with_rule,
        status='active'
    ).order_by('row_id', 'number').only('id', 'row_id', 'number', 'display_number')

    for seat in all_seats:
        if seat.row_id not in all_seats_map:
            all_seats_map[seat.row_id] = []
        all_seats_map[seat.row_id].append(seat)

    existing_reservations = set(
        SeatReservation.objects.filter(
            performance=performance,
            seat__row_id__in=row_ids_with_rule,
            status__in=['reserved', 'sold', 'blocked']
        ).values_list('seat_id', flat=True)
    )

    for row_id in row_ids_with_rule:
        seat_ids_in_row = rows_to_check[row_id]['seat_ids']
        all_seats_in_row = all_seats_map.get(row_id, [])

        if not all_seats_in_row:
            continue

        # Simulate occupied seats
        occupied_seats = existing_reservations | set(seat_ids_in_row)

        # Check orphan
        for i, seat in enumerate(all_seats_in_row):
            if seat.id in occupied_seats:
                continue

            has_left = (i > 0 and all_seats_in_row[i-1].id in occupied_seats)
            has_right = (i < len(all_seats_in_row) - 1 and
                         all_seats_in_row[i+1].id in occupied_seats)

            if has_left and has_right:
                return (
                    False,
                    f'Không thể đặt vì sẽ để lại ghế {seat.full_display_label} trống ở giữa. '
                    f'Vui lòng chọn ghế khác hoặc thêm ghế này vào.'
                )

    return (True, None)


def get_performance_seat_map(performance):
    """Get complete seat map for a performance - OPTIMIZED"""
    venue = performance.show.venue
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
            ).only('seat_id', 'status'),
            to_attr='active_reservations'
        )
    )

    performance_prices = PerformancePrice.objects.filter(
        performance=performance
    ).values('price_category_id', 'price')
    price_map = {pp['price_category_id']: pp['price'] for pp in performance_prices}

    utc_plus_7 = dt_timezone(timedelta(hours=7))
    datetime_in_utc7 = performance.datetime.astimezone(utc_plus_7)

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

        # ✅ Determine seat status from prefetched data (NO extra query)
        seat_status = (
            seat.active_reservations[0].status
            if seat.active_reservations
            else 'available'
        )

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
            'actual_seat_numbers': [s.number for s in row_data['seats']],
        }

    from venues.models import PriceCategory
    all_categories = PriceCategory.objects.all().order_by('base_price')

    seat_map_data['price_categories'] = {}
    for pc in all_categories:
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
    from .utils import validate_session_ownership
    serializer = ReserveSeatSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    performance_id = serializer.validated_data['performance_id']
    seat_ids = serializer.validated_data['seat_ids']
    session_id = serializer.validated_data['session_id']

    if not validate_session_ownership(session_id, request):
        logger.warning(f"⚠️ Potential session hijacking: {session_id}")
        return Response(
            {'error': 'Session không hợp lệ'},
            status=status.HTTP_403_FORBIDDEN
        )
    performance = Performance.objects.get(id=performance_id)
    client_ip = request.META.get('REMOTE_ADDR')
    with transaction.atomic():
        # Release expired reservations that are not linked to any booking yet
        expired_reservations = SeatReservation.objects.filter(
            performance=performance,
            status='reserved',
            expires_at__lt=timezone.now(),
            booking__isnull=True
        )
        expired_reservations.update(status='available', session_id='', expires_at=None, client_ip=None)

        existing_session_reservations = SeatReservation.objects.filter(
            performance=performance,
            session_id=session_id,
            status='reserved',
            expires_at__gt=timezone.now()
        )

        existing_seat_ids = set(existing_session_reservations.values_list('seat_id', flat=True))
        new_seat_ids = set(seat_ids)
        total_seat_ids = existing_seat_ids | new_seat_ids  # Union of both sets

        if len(total_seat_ids) > 8:
            return Response(
                {
                    'error': f'Không thể giữ quá 8 ghế. Bạn đang có {len(existing_seat_ids)} ghế, yêu cầu thêm {len(new_seat_ids)} ghế.',
                    'current_count': len(existing_seat_ids),
                    'requested_count': len(new_seat_ids),
                    'max_allowed': 8
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check if any requested seats are already reserved (by another session) or sold
        conflicting_reservations = SeatReservation.objects.filter(
            performance=performance,
            seat_id__in=seat_ids,
            status__in=['reserved', 'sold']
        ).exclude(session_id=session_id)

        if conflicting_reservations.exists():
            return Response(
                {'error': 'Một số ghế đã được đặt hoặc đang được giữ bởi người khác. Vui lòng tải lại trang.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        is_valid, error_msg = validate_orphan_seats(seat_ids, performance)
        if not is_valid:
            return Response(
                {'error': error_msg},
                status=status.HTTP_400_BAD_REQUEST
            )

        seats = Seat.objects.filter(id__in=seat_ids).select_related(
            'row', 'row__section', 'row__price_category', 'price_category'
        )
        seat_dict = {seat.id: seat for seat in seats}

        if len(seat_dict) != len(set(seat_ids)):
            return Response({'error': 'Một hoặc nhiều ghế không hợp lệ.'}, status=status.HTTP_400_BAD_REQUEST)

        # Get performance prices
        performance_prices = PerformancePrice.objects.filter(
            performance=performance
        ).values('price_category_id', 'price')
        price_map = {pp['price_category_id']: pp['price'] for pp in performance_prices}

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
            seat = seat_dict[seat_id]
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
                    'price': seat_price,
                    'expires_at': expires_at,
                    'client_ip': client_ip,
                    'booking': None
                }
            )

            reserved_seats.append({
                'id': seat.id,
                'row': seat.row.label,
                'number': seat.display_label,
                'full_label': seat.full_display_label,
                'section_name': seat.row.section.name,
                'price': float(seat_price)
            })

        BookingHistory.log_action(
            booking=None,
            action='reserve_seat',
            request=request,
            seats=SeatReservation.objects.filter(
                performance=performance,
                seat_id__in=seat_ids,
                session_id=session_id
            ),
            session_id=session_id,
            extra_data={
                'performance_id': performance_id,
                'seat_count': len(seat_ids)
            }
        )

    return Response({
        'seats': reserved_seats,
        'expires_at': expires_at.isoformat(),
        'timeout_seconds': timeout_minutes * 60
    })


@api_view(['POST'])
@csrf_exempt
def release_seats(request):
    """
    Release reserved seats that are NOT associated with a booking.
    This is the key fix to prevent releasing seats for a pending payment.
    """
    session_id = request.data.get('session_id')
    seat_ids = request.data.get('seat_ids', [])

    if not session_id:
        return Response(
            {'error': 'session_id is required'},
            status=status.HTTP_400_BAD_REQUEST
        )

    # CRITICAL FIX: Only release seats that are temporarily reserved and NOT yet part of a booking.
    reservations_to_release = SeatReservation.objects.filter(
        session_id=session_id,
        seat_id__in=seat_ids,
        status='reserved',
        booking__isnull=True  # This ensures we don't release seats for a pending payment.
    )

    count = reservations_to_release.update(
        status='available',
        session_id='',
        expires_at=None,
        client_ip=None
    )

    if count > 0:
        BookingHistory.log_action(
            booking=None,
            action='seat_released',
            request=request,
            seats=None,  # đã release rồi
            session_id=session_id,
            extra_data={
                'released_count': count,
                'seat_ids': seat_ids
            }
        )

    return Response({'released': count})


@api_view(['GET'])
def search_bookings(request):
    """
    Search for bookings by booking code or customer phone number.
    Only returns paid bookings for performances that happened yesterday or are in the future.
    """
    search_query = request.query_params.get('search', None)
    if not search_query:
        return Response(
            {'error': 'Vui lòng cung cấp mã vé hoặc số điện thoại để tra cứu.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    cutoff_date = timezone.now().date() - timedelta(days=1)

    bookings = Booking.objects.filter(
        Q(booking_code__iexact=search_query) | Q(customer_phone__exact=search_query),
        status='paid',
        performance__datetime__date__gte=cutoff_date
    ).select_related(
        'performance',
        'performance__show',
        'performance__show__venue'
    ).prefetch_related(
        Prefetch(
            'seat_reservations',
            queryset=SeatReservation.objects.select_related(
                'seat', 'seat__row', 'seat__row__section'
            )
        )
    ).order_by('-performance__datetime')

    if not bookings.exists():
        return Response([], status=status.HTTP_200_OK)

    serializer = BookingDetailSerializer(bookings, many=True)
    return Response(serializer.data)


@method_decorator(csrf_exempt, name='dispatch')
class BookingViewSet(viewsets.ModelViewSet):
    """API for Bookings"""
    queryset = Booking.objects.all()
    serializer_class = BookingDetailSerializer
    lookup_field = 'booking_code'

    def get_queryset(self):
        """
        Override to apply select_related and prefetch_related to all lookups.
        """
        return Booking.objects.all().select_related(
            'performance',
            'performance__show',
            'performance__show__venue'
        ).prefetch_related(
            Prefetch(
                'seat_reservations',
                queryset=SeatReservation.objects.select_related(
                    'seat', 'seat__row', 'seat__row__section'
                )
            )
        )

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

        optimized_booking = self.get_queryset().get(pk=booking.pk)
        detail_serializer = BookingDetailSerializer(optimized_booking)
        response_data = detail_serializer.data

        response_data['expires_at'] = optimized_booking.expires_at.isoformat()
        response_data['timeout_seconds'] = int((optimized_booking.expires_at - timezone.now()).total_seconds())

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
            seats_to_log = list(booking.seat_reservations.all())

            booking.status = 'cancelled'
            booking.save()

            # Release seats
            booking.seat_reservations.update(
                status='available',
                session_id='',
                expires_at=None,
                booking=None
            )

            BookingHistory.log_action(
                booking=booking,
                action='booking_cancelled',
                request=request,
                seats=seats_to_log,
                extra_data={'cancelled_by': 'user'}
            )

        return Response({'status': 'cancelled'})

    @action(detail=True, methods=['post'], url_path='resend-email')
    def resend_email(self, request, booking_code=None):
        """Resend booking confirmation email"""
        booking = self.get_object()

        if booking.status not in ['paid']:
            return Response(
                {'error': 'Chỉ có thể gửi lại email cho đơn đã thanh toán'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
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


@api_view(['GET'])
@csrf_exempt
def get_session_reservations(request):
    """
    Get all reserved seats for a session
    Used to restore seats after page refresh
    """
    session_id = request.query_params.get('session_id')
    performance_id = request.query_params.get('performance_id')

    empty_response = {
        'seats': [],
        'expires_at': None,
        'count': 0
    }

    if not session_id or not performance_id:
        return Response(empty_response)

    try:
        performance = Performance.objects.get(id=performance_id)

        # We only care about reservations not yet linked to a final booking
        reservations = SeatReservation.objects.filter(
            performance=performance,
            session_id=session_id,
            status='reserved',
            booking__isnull=True,
            expires_at__gt=timezone.now()
        ).select_related('seat', 'seat__row', 'seat__row__section')

        if not reservations.exists():
            return Response(empty_response)

        first_reservation = reservations.first()
        expires_at = first_reservation.expires_at

        reserved_seats = []
        for reservation in reservations:
            seat = reservation.seat
            reserved_seats.append({
                'id': seat.id,
                'row': seat.row.label,
                'number': seat.display_label,
                'full_label': seat.full_display_label,
                'section_name': seat.row.section.name,
                'price': float(reservation.price)
            })

        return Response({
            'seats': reserved_seats,
            'expires_at': expires_at.isoformat(),
            'count': len(reserved_seats)
        })

    except Exception as e:
        logger.error(f"get_session_reservations: Unexpected error: {e}", exc_info=True)
        return Response(empty_response)
