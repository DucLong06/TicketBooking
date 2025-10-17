from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Discount
from .services import validate_and_calculate_discount, DiscountError
from bookings.models import Booking, Discount, SeatReservation
from django.utils import timezone
from django.db.models import Q, F
from logzero import logger


@api_view(['POST'])
def validate_discount_code(request):
    code = request.data.get('code', '').strip()
    session_id = request.data.get('session_id')
    email = request.data.get('customer_email', '')
    phone = request.data.get('customer_phone', '')

    logger.info(f"🔍 Validating discount: code={code}, session={session_id}")

    if not code:
        return Response({'error': 'Vui lòng nhập mã giảm giá'}, status=status.HTTP_400_BAD_REQUEST)

    if not session_id:
        return Response({'error': 'Session không hợp lệ'}, status=status.HTTP_400_BAD_REQUEST)

    seat_reservations = SeatReservation.objects.filter(
        session_id=session_id,
        status='reserved',
        booking__isnull=True
    )

    seat_count = seat_reservations.count()
    logger.info(f"🔍 Found {seat_count} seats for session {session_id}")

    if not seat_reservations.exists():
        return Response({'error': 'Không tìm thấy ghế đã chọn'}, status=status.HTTP_400_BAD_REQUEST)

    total_amount = sum(sr.price for sr in seat_reservations)
    logger.info(f"🔍 Total amount: {total_amount}")

    temp_booking = Booking(
        total_amount=total_amount,
        customer_email=email,
        customer_phone=phone,
        session_id=session_id
    )

    temp_booking._temp_seat_count = seat_count

    logger.info(f"🔍 Temp booking seat count: {temp_booking._temp_seat_count}")

    try:
        discount, discount_amount = validate_and_calculate_discount(
            booking=temp_booking,
            code=code
        )

        logger.info(f"✅ Discount validated: {discount.code}, amount={discount_amount}")

        return Response({
            'valid': True,
            'code': discount.code,
            'description': str(discount),
            'discount_amount': float(discount_amount),
            'message': f'Áp dụng thành công! Bạn được giảm {discount_amount:,.0f}đ'
        })

    except DiscountError as e:
        logger.warning(f"❌ Discount error: {str(e)}")
        return Response(
            {'valid': False, 'error': str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['GET'])
def get_available_discounts(request):

    ticket_count = int(request.GET.get('ticket_count', 0))
    email = request.GET.get('email', '')
    phone = request.GET.get('phone', '')
    include_unavailable = request.GET.get('include_unavailable', 'false').lower() == 'true'

    now = timezone.now()

    discounts = Discount.objects.filter(
        is_active=True,
        valid_from__lte=now,
    ).filter(
        Q(valid_to__isnull=True) | Q(valid_to__gte=now)
    )

    # Filter by ticket quantity
    if ticket_count > 0:
        discounts = discounts.filter(
            Q(min_ticket_quantity__isnull=True) |
            Q(min_ticket_quantity__lte=ticket_count)
        )

    # Filter by user eligibility
    eligible_discounts = []
    unavailable_discounts = []

    for discount in discounts:
        has_usage_left = (
            discount.max_usage is None or
            discount.usage_count < discount.max_usage
        )

        is_user_valid, message = discount.is_valid(
            user_email=email,
            user_phone=phone,
            ticket_quantity=ticket_count
        )

        discount_data = {
            'code': discount.code,
            'description': str(discount),
            'min_ticket_quantity': discount.min_ticket_quantity,
            'discount_type': discount.discount_type,
            'value': float(discount.value),
            'max_usage': discount.max_usage,
            'usage_count': discount.usage_count,
        }

        if is_user_valid and has_usage_left:
            eligible_discounts.append({**discount_data, 'eligible': True})
        elif include_unavailable:
            reason = message if not has_usage_left else "Mã đã hết lượt sử dụng"
            unavailable_discounts.append({
                **discount_data,
                'eligible': False,
                'reason': reason
            })

    response_data = {'discounts': eligible_discounts}
    if include_unavailable:
        response_data['unavailable_discounts'] = unavailable_discounts

    return Response(response_data)
