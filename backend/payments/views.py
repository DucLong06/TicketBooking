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
from bookings.models import Booking
from discounts.models import DiscountUsage


@api_view(['POST'])
def create_payment(request, booking_code):
    """Create payment for booking with 9Pay"""
    booking = get_object_or_404(Booking, booking_code=booking_code)

    if booking.status != 'pending':
        return Response(
            {'error': 'Booking không ở trạng thái chờ thanh toán'},
            status=status.HTTP_400_BAD_REQUEST
        )

    payment_method = '9pay'
    transaction_id = f"TXN{uuid.uuid4().hex[:10].upper()}"

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
        return Response({
            'payment_url': payment_url,
            'transaction_id': transaction_id,
            'amount': float(booking.final_amount),
            'method': '9pay'
        })
    else:
        logger.error("Failed to create 9Pay payment URL")
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
        payment = Payment.objects.select_related('booking').get(transaction_id=transaction_id)
        booking = payment.booking

        if payment_status_code == 5 and error_code == '000':
            logger.info(f"✅ Payment {transaction_id} successful")

            with transaction.atomic():
                payment.status = 'success'
                payment.paid_at = timezone.now()
                payment.gateway_response = payment_data
                payment.gateway_transaction_id = payment_data.get('payment_no')
                payment.save()

                booking.status = 'paid'
                booking.paid_at = timezone.now()
                booking.save()

                booking.seat_reservations.update(status='sold')

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
