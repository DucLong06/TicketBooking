from decimal import Decimal
from .models import Discount, DiscountUsage
from bookings.models import Booking
from django.db import transaction


class DiscountError(Exception):
    """Custom exception for discount errors."""
    pass


def validate_and_calculate_discount(booking: Booking, code: str):
    """
    Validates a discount code and calculates the discount amount for a given booking.
    This is the single source of truth for discount logic.

    Args:
        booking: The Booking instance.
        code: The discount code string.

    Returns:
        A tuple of (discount_instance, discount_amount).

    Raises:
        DiscountError: If the discount is invalid for any reason.
    """
    if not code:
        raise DiscountError('Vui lòng cung cấp mã giảm giá.')

    with transaction.atomic():
        try:
            discount = Discount.objects.select_for_update().get(code__iexact=code)
        except Discount.DoesNotExist:
            raise DiscountError('Mã giảm giá không hợp lệ.')

        # 1. Validate discount activity, expiry, etc.
        is_valid, message = discount.is_valid(
            user_email=booking.customer_email,
            user_phone=booking.customer_phone
        )
        if not is_valid:
            raise DiscountError(message)

        # 2. Check usage limit (including pending ones)
        pending_usages = DiscountUsage.objects.filter(
            discount=discount, status='PENDING'
        ).exclude(booking=booking).count()

        if discount.max_usage is not None and (discount.usage_count + pending_usages) >= discount.max_usage:
            raise DiscountError('Mã giảm giá đã hết lượt sử dụng.')

        # NEW: Check minimum ticket quantity
        if discount.min_ticket_quantity:
            ticket_count = booking.seat_reservations.count() if booking.pk else 0

            # For new bookings during creation, count from seat_ids
            if ticket_count == 0:
                from bookings.models import SeatReservation
                ticket_count = SeatReservation.objects.filter(
                    booking__isnull=True,
                    session_id=booking.session_id
                ).count()

            if ticket_count < discount.min_ticket_quantity:
                raise DiscountError(
                    f'Mã này yêu cầu mua tối thiểu {discount.min_ticket_quantity} vé. '
                    f'Bạn đang mua {ticket_count} vé.'
                )

        # 3. Calculate discount amount (only on ticket total, not service fee)
        ticket_total = booking.total_amount
        discount_amount = Decimal('0')

        if discount.discount_type == 'PERCENTAGE':
            calculated_amount = (ticket_total * discount.value) / Decimal('100.00')
            discount_amount = calculated_amount.quantize(Decimal('1'))
        elif discount.discount_type == 'FIXED_AMOUNT':
            discount_amount = discount.value.quantize(Decimal('1'))

        # The discount cannot be greater than the ticket total
        discount_amount = min(ticket_total, discount_amount)

        return discount, discount_amount
