from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Discount
from .services import validate_and_calculate_discount, DiscountError
from bookings.models import Booking, Discount, SeatReservation
from django.utils import timezone
from django.db.models import Q, F


@api_view(['POST'])
def validate_discount_code(request):
    """
    Validate discount code WITHOUT creating a booking
    Payload: {
        "code": "SALE50",
        "session_id": "session_xxx",
        "customer_email": "user@example.com",
        "customer_phone": "0912345678"
    }
    """
    code = request.data.get('code', '').strip()
    session_id = request.data.get('session_id')
    email = request.data.get('customer_email', '')
    phone = request.data.get('customer_phone', '')

    if not code:
        return Response(
            {'error': 'Vui lòng nhập mã giảm giá'},
            status=status.HTTP_400_BAD_REQUEST
        )

    if not session_id:
        return Response(
            {'error': 'Session không hợp lệ'},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Get reserved seats for this session
    seat_reservations = SeatReservation.objects.filter(
        session_id=session_id,
        status='reserved',
        booking__isnull=True
    )

    if not seat_reservations.exists():
        return Response(
            {'error': 'Không tìm thấy ghế đã chọn'},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Calculate total
    total_amount = sum(sr.price for sr in seat_reservations)

    # Create temporary booking object (NOT saved to DB)
    temp_booking = Booking(
        total_amount=total_amount,
        customer_email=email,
        customer_phone=phone,
        session_id=session_id
    )

    # Attach seat count for validation
    temp_booking._temp_seat_count = seat_reservations.count()

    try:
        discount, discount_amount = validate_and_calculate_discount(
            booking=temp_booking,
            code=code
        )

        return Response({
            'valid': True,
            'code': discount.code,
            'description': str(discount),
            'discount_amount': float(discount_amount),
            'message': f'Áp dụng thành công! Bạn được giảm {discount_amount:,.0f}đ'
        })

    except DiscountError as e:
        return Response(
            {'valid': False, 'error': str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['GET'])
def get_available_discounts(request):
    """
    Get available discount codes based on ticket quantity
    Query params:
    - ticket_count: number of tickets
    - email: customer email (optional)
    - phone: customer phone (optional)
    """
    ticket_count = int(request.GET.get('ticket_count', 0))
    email = request.GET.get('email', '')
    phone = request.GET.get('phone', '')

    now = timezone.now()

    # Base queryset: active, not expired, has usage left
    discounts = Discount.objects.filter(
        is_active=True,
        valid_from__lte=now,
    ).filter(
        Q(valid_to__isnull=True) | Q(valid_to__gte=now)
    ).filter(
        Q(max_usage__isnull=True) | Q(usage_count__lt=F('max_usage'))
    )

    # Filter by ticket quantity
    if ticket_count > 0:
        discounts = discounts.filter(
            Q(min_ticket_quantity__isnull=True) |
            Q(min_ticket_quantity__lte=ticket_count)
        )

    # Filter by user eligibility
    eligible_discounts = []
    for discount in discounts:
        is_valid, _ = discount.is_valid(user_email=email, user_phone=phone)
        if is_valid:
            eligible_discounts.append({
                'code': discount.code,
                'description': str(discount),
                'min_ticket_quantity': discount.min_ticket_quantity,
                'discount_type': discount.discount_type,
                'value': float(discount.value)
            })

    return Response({'discounts': eligible_discounts})
