import uuid
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404, redirect
from django.db import transaction
from django.utils import timezone
from django.conf import settings
from logzero import logger

from .models import Payment
from .ninepay import NinePay
from bookings.models import Booking, SeatReservation, BookingHistory
from discounts.models import DiscountUsage


@api_view(['POST'])
def create_payment(request, booking_code):
    """Create payment for booking with 9Pay"""
    with transaction.atomic():
        booking = get_object_or_404(
            Booking.objects.select_for_update().select_related(
                'performance__show'
            ),
            booking_code=booking_code
        )

        if booking.status != 'pending':
            return Response(
                {'error': 'Booking không ở trạng thái chờ thanh toán'},
                status=status.HTTP_400_BAD_REQUEST
            )

        seat_reservations = booking.seat_reservations.select_for_update().filter(
            status='reserved',
            expires_at__gt=timezone.now()
        )

        if seat_reservations.count() == 0:
            logger.error(f"🚨 CRITICAL: Booking {booking_code} has NO VALID SEATS")
            booking.status = 'cancelled'
            booking.save()
            return Response(
                {'error': 'Booking không có ghế hợp lệ. Vui lòng đặt lại.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        expected_seat_count = booking.seat_reservations.count()
        if seat_reservations.count() != expected_seat_count:
            logger.error(f"🚨 Seat mismatch: {seat_reservations.count()} valid vs {expected_seat_count} total")
            booking.status = 'cancelled'
            booking.save()
            seat_reservations.update(status='available', session_id=None, expires_at=None)
            return Response(
                {'error': 'Có ghế không hợp lệ. Vui lòng đặt lại.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        duplicate_check = SeatReservation.objects.filter(
            seat_id__in=seat_reservations.values_list('seat_id', flat=True),
            performance=booking.performance,
            status__in=['reserved', 'sold']
        ).exclude(booking=booking)

        if duplicate_check.exists():
            logger.error(f"🚨 CRITICAL: Booking {booking_code} has duplicate seats")
            booking.status = 'cancelled'
            booking.save()
            seat_reservations.update(status='available', session_id=None, expires_at=None)
            return Response(
                {'error': 'Có ghế bị trùng. Vui lòng đặt lại.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        calculated_ticket_amount = sum(sr.price for sr in seat_reservations)
        calculated_service_fee = seat_reservations.count() * booking.performance.show.service_fee_per_ticket
        calculated_shipping_fee = booking.shipping_fee
        calculated_final = calculated_ticket_amount + calculated_shipping_fee + calculated_service_fee - booking.discount_amount

        if abs(calculated_final - booking.final_amount) > 1:  # Allow 1đ rounding error
            logger.error(f"🚨 AMOUNT MISMATCH: calculated={calculated_final}, stored={booking.final_amount}")
            booking.status = 'cancelled'
            booking.save()
            return Response(
                {'error': 'Số tiền không khớp. Vui lòng đặt lại.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if booking.expires_at and booking.expires_at < timezone.now():
            logger.error(f"🚨 Booking {booking_code} expired at {booking.expires_at}")
            booking.status = 'expired'
            booking.save()
            seat_reservations.update(status='available', session_id=None, expires_at=None)
            return Response(
                {'error': 'Booking đã hết hạn. Vui lòng đặt lại.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        payment_method = '9pay'
        transaction_id = f"DCA{uuid.uuid4().hex[:10].upper()}"

        payment = Payment.objects.create(
            booking=booking,
            transaction_id=transaction_id,
            payment_method=payment_method,
            amount=booking.final_amount,
            status='pending'
        )

    ninepay = NinePay()

    logger.info(f"Creating 9Pay payment for booking {booking.booking_code}")
    logger.info(f"Transaction ID: {transaction_id}")
    logger.info(f"Amount: {booking.final_amount}")

    payment_url = ninepay.get_payment_url(
        invoice_no=transaction_id,
        amount=booking.final_amount,
        description=f"Thanh toan ve {booking.booking_code}",
        return_url=settings.NINEPAY_RETURN_URL,
        back_url=f'{settings.FRONTEND_URL}/payment'
    )

    if payment_url:
        logger.info(f"9Pay payment URL created successfully")

        BookingHistory.log_action(
            booking=booking,
            action='payment_initiated',
            request=request,
            seats=seat_reservations,
            payment_amount=booking.final_amount,
            payment_status='pending',
            gateway_response=payment_url,
            extra_data={
                'transaction_id': payment.transaction_id,
                'payment_method': payment.payment_method
            }
        )
        return Response({
            'payment_url': payment_url,
            'transaction_id': transaction_id,
            'amount': float(booking.final_amount),
            'method': '9pay'
        })
    else:
        logger.error("Failed to create 9Pay payment URL")
        BookingHistory.log_action(
            booking=booking,
            action='payment_failed',
            request=request,
            seats=seat_reservations,
            error=payment_url,
            gateway_response=payment_url
        )
        return Response(
            {'error': 'Không thể tạo yêu cầu thanh toán với 9Pay'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET', 'POST'])
def ninepay_return(request):
    """Handle 9Pay return callback"""
    params = request.GET.dict() if request.method == 'GET' else request.POST.dict()

    logger.info(f"===== 9Pay Return Callback =====")
    logger.debug(f"Full params: {params}")

    ninepay = NinePay()

    if not ninepay.verify_return(params):
        logger.error("Invalid signature/checksum")
        return redirect(f'{settings.FRONTEND_URL}/payment/error?reason=invalid_signature')

    payment_data = ninepay.parse_return_data(params)

    if not payment_data:
        logger.error("Failed to parse payment data")
        return redirect(f'{settings.FRONTEND_URL}/payment/error?reason=parse_error')

    transaction_id = payment_data.get('invoice_no')
    payment_status_code = payment_data.get('status')
    error_code = str(payment_data.get('error_code', ''))

    logger.info(f"Transaction {transaction_id} - Status: {payment_status_code}, Error code: {error_code}")

    if not transaction_id:
        logger.error("Missing invoice_no")
        return redirect(f'{settings.FRONTEND_URL}/payment/error?reason=missing_invoice')

    try:
        with transaction.atomic():
            payment = Payment.objects.select_for_update().get(transaction_id=transaction_id)
            booking = Booking.objects.select_for_update().get(id=payment.booking_id)

            if payment.status == 'success' and booking.status == 'paid':
                logger.warning(f"⚠️ Payment {transaction_id} already processed successfully")
                return redirect(f'{settings.FRONTEND_URL}/booking/confirmation/{booking.booking_code}')

            if payment.status == 'failed' and booking.status == 'cancelled':
                logger.warning(f"⚠️ Payment {transaction_id} already processed as failed")
                return redirect(f'{settings.FRONTEND_URL}/payment/failed')

            if booking.status not in ['pending', 'paid']:
                logger.error(f"🚨 Invalid booking status: {booking.status}")
                return redirect(f'{settings.FRONTEND_URL}/payment/error?reason=invalid_booking_status')

            if payment_status_code == 5 and error_code == '000':
                logger.info(f"✅ Payment {transaction_id} successful")

                payment.status = 'success'
                payment.paid_at = timezone.now()
                payment.gateway_response = payment_data
                payment.gateway_transaction_id = payment_data.get('payment_no')
                payment.save()

                booking.status = 'paid'
                booking.paid_at = timezone.now()
                booking.save()

                old_session = booking.session_id
                booking.session_id = ''
                booking.save()

                logger.info(f"Cleared session_id '{old_session}' for booking {booking.booking_code}")

                seat_reservations = booking.seat_reservations.select_for_update().filter(
                    status='reserved'
                )

                seat_count = seat_reservations.count()
                updated = seat_reservations.update(status='sold')

                logger.info(f"Seats: {seat_count}, Updated: {updated}")

                if updated == 0:
                    logger.error(f"🚨 CRITICAL: Payment OK but NO SEATS updated for {booking.booking_code}")
                elif updated != seat_count:
                    logger.warning(f"⚠️ Seat update mismatch: expected {seat_count}, updated {updated}")

                try:
                    usage = DiscountUsage.objects.select_for_update().get(booking=booking, status='PENDING')
                    usage.status = 'COMPLETED'
                    usage.save()

                    discount = usage.discount
                    discount.usage_count += 1
                    discount.save()
                    logger.info(
                        f"✅ Discount code '{discount.code}' usage confirmed for booking {booking.booking_code}.")
                except DiscountUsage.DoesNotExist:
                    pass

                from bookings.email_service import send_booking_confirmation
                try:
                    send_booking_confirmation(booking)
                except Exception as e:
                    logger.error(f"Failed to send confirmation email: {e}")

                BookingHistory.log_action(
                    booking=booking,
                    action='payment_success',
                    request=request,
                    seats=booking.seat_reservations.all(),
                    payment_amount=booking.final_amount,
                    payment_status='success',
                    gateway_response=payment_data
                )

                return redirect(f'{settings.FRONTEND_URL}/booking/confirmation/{booking.booking_code}')

            else:
                logger.warning(
                    f"❌ Payment {transaction_id} failed - Status: {payment_status_code}, Error code: {error_code}")

                payment.status = 'failed'
                payment.gateway_response = payment_data
                payment.save()

                if booking.status == 'pending':
                    booking.status = 'cancelled'
                    booking.save()
                    booking.seat_reservations.update(status='available', session_id=None, expires_at=None)

                try:
                    usage = DiscountUsage.objects.select_for_update().get(booking=booking, status='PENDING')
                    usage.status = 'CANCELLED'
                    usage.save()
                    logger.warning(
                        f"❌ Discount code '{usage.discount.code}' usage cancelled for booking {booking.booking_code}.")
                except DiscountUsage.DoesNotExist:
                    pass

                failure_reason = payment_data.get('failure_reason', 'Giao dịch thất bại')
                failure_url = f'{settings.FRONTEND_URL}/payment/failed?code={error_code}&message={failure_reason}'

                BookingHistory.log_action(
                    booking=booking,
                    action='payment_failed',
                    request=request,
                    seats=booking.seat_reservations.all(),
                    payment_amount=booking.final_amount,
                    payment_status='failed',
                    gateway_response=payment_data,
                    error=f"Payment failed with status {status}, error_code {error_code}"
                )

                return redirect(failure_url)

    except Payment.DoesNotExist:
        logger.error(f"Payment not found: {transaction_id}")
        return redirect(f'{settings.FRONTEND_URL}/payment/error?reason=payment_not_found')
    except Exception as e:
        logger.error(f"Error processing payment callback: {e}", exc_info=True)
        return redirect(f'{settings.FRONTEND_URL}/payment/error?reason=server_error')


@api_view(['GET'])
def check_payment_status(request, transaction_id):
    """Check payment status"""
    payment = get_object_or_404(Payment, transaction_id=transaction_id)

    return Response({
        'transaction_id': payment.transaction_id,
        'status': payment.status,
        'amount': float(payment.amount),
        'paid_at': payment.paid_at.isoformat() if payment.paid_at else None,
        'booking_code': payment.booking.booking_code,
        'booking_status': payment.booking.status
    })
