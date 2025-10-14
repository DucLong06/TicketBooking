from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from django.db import transaction
from decimal import Decimal

from .models import Discount, DiscountUsage
from bookings.models import Booking
from bookings.serializers import BookingDetailSerializer


@api_view(['POST'])
@transaction.atomic
def apply_discount(request):
    code = request.data.get('code')
    booking_code = request.data.get('booking_code')

    if not code or not booking_code:
        return Response({'error': 'Vui lòng cung cấp mã giảm giá và mã đơn hàng.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        booking = Booking.objects.select_for_update().get(booking_code=booking_code)
    except Booking.DoesNotExist:
        return Response({'error': 'Đơn hàng không tồn tại.'}, status=status.HTTP_404_NOT_FOUND)

    if booking.status != 'pending':
        return Response({'error': 'Chỉ có thể áp dụng mã giảm giá cho đơn hàng đang chờ thanh toán.'}, status=status.HTTP_400_BAD_REQUEST)

    if booking.discount:
        return Response({'error': 'Đơn hàng đã được áp dụng một mã giảm giá khác.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        discount = Discount.objects.get(code__iexact=code)
    except Discount.DoesNotExist:
        return Response({'error': 'Mã giảm giá không tồn tại.'}, status=status.HTTP_404_NOT_FOUND)

    # Validate discount
    is_valid, message = discount.is_valid(user_email=booking.customer_email, user_phone=booking.customer_phone)
    if not is_valid:
        return Response({'error': message}, status=status.HTTP_400_BAD_REQUEST)

    # Check for pending usages by other bookings
    pending_usages = DiscountUsage.objects.filter(discount=discount, status='PENDING').exclude(booking=booking).count()
    if discount.max_usage is not None and (discount.usage_count + pending_usages) >= discount.max_usage:
        return Response({'error': 'Mã giảm giá này đang được người khác sử dụng. Vui lòng thử lại sau.'}, status=status.HTTP_400_BAD_REQUEST)

    # Calculate discount amount
    original_total = booking.total_amount + booking.service_fee
    discount_amount = Decimal('0.00')
    if discount.discount_type == 'PERCENTAGE':
        discount_amount = (original_total * discount.value) / Decimal('100.00')
    elif discount.discount_type == 'FIXED_AMOUNT':
        discount_amount = discount.value

    # Ensure discount doesn't exceed total amount
    discount_amount = min(original_total, discount_amount)

    # Update booking
    booking.discount = discount
    booking.discount_amount = discount_amount
    booking.final_amount = original_total - discount_amount
    booking.save()

    # Create usage record
    DiscountUsage.objects.create(discount=discount, booking=booking, status='PENDING')

    serializer = BookingDetailSerializer(booking)
    return Response(serializer.data)
