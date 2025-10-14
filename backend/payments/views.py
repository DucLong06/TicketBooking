import uuid
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404, redirect
from django.db import transaction
from django.utils import timezone
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from logzero import logger

from .models import Payment
from .ninepay import NinePay
from bookings.models import Booking


@api_view(['POST'])
def create_payment(request, booking_code):
    """Create payment for booking with 9Pay"""
    booking = get_object_or_404(Booking, booking_code=booking_code)

    if booking.status != 'pending':
        return Response(
            {'error': 'Booking không ở trạng thái chờ thanh toán'},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Always use 9Pay
    payment_method = '9pay'
    transaction_id = f"TXN{uuid.uuid4().hex[:10].upper()}"

    # Create payment record
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
    logger.info(f"Method: {request.method}")
    logger.info(f"Params keys: {list(params.keys())}")
    logger.debug(f"Full params: {params}")

    ninepay = NinePay()

    # Verify signature/checksum
    if not ninepay.verify_return(params):
        logger.error("Invalid signature/checksum")
        return redirect(f'{settings.FRONTEND_URL}/payment/error?reason=invalid_signature')

    # Parse payment data
    payment_data = ninepay.parse_return_data(params)

    if not payment_data:
        logger.error("Failed to parse payment data")
        return redirect(f'{settings.FRONTEND_URL}/payment/error?reason=parse_error')

    logger.info(f"Parsed payment data: {payment_data}")

    # Extract transaction info
    transaction_id = payment_data.get('invoice_no')
    status = payment_data.get('status')  # This is int from 9Pay
    error_code = str(payment_data.get('error_code', ''))  # Ensure string

    logger.info(
        f"Transaction {transaction_id} - Status: {status} (type: {type(status).__name__}), Error code: {error_code}")

    if not transaction_id:
        logger.error("Missing invoice_no")
        return redirect(f'{settings.FRONTEND_URL}/payment/error?reason=missing_invoice')

    try:
        payment = Payment.objects.get(transaction_id=transaction_id)
        booking = payment.booking

        # Check status
        # status: 5 = success, error_code: "000" = success
        # 9Pay returns status as integer 5, not string
        if status == 5 and error_code == '000':
            logger.info(f"✅ Payment {transaction_id} successful - Status: {status}, Error: {error_code}")

            with transaction.atomic():
                # Update payment
                payment.status = 'success'
                payment.paid_at = timezone.now()
                payment.gateway_response = payment_data
                payment.gateway_transaction_id = payment_data.get('payment_no')
                payment.save()

                # Update booking
                booking.status = 'paid'
                booking.paid_at = timezone.now()
                booking.save()

                # Update seats
                booking.seat_reservations.update(status='sold')

                # Send confirmation email
                from bookings.email_service import send_booking_confirmation
                try:
                    send_booking_confirmation(booking)
                except Exception as e:
                    logger.error(f"Failed to send email: {e}")

            # Redirect to success page
            logger.info(f"Redirecting to confirmation page")
            return redirect(f'{settings.FRONTEND_URL}/booking/confirmation/{booking.booking_code}')

        else:
            # Payment failed
            logger.warning(
                f"❌ Payment {transaction_id} failed - Status: {status} (expected 5), Error code: {error_code} (expected '000')")

            payment.status = 'failed'
            payment.gateway_response = payment_data
            payment.save()

            failure_reason = payment_data.get('failure_reason', 'Unknown error')
            failure_url = f'{settings.FRONTEND_URL}/payment/failed?code={error_code}&message={failure_reason}'
            return redirect(failure_url)

    except Payment.DoesNotExist:
        logger.error(f"Payment not found: {transaction_id}")
        return redirect(f'{settings.FRONTEND_URL}/payment/error?reason=payment_not_found')
    except Exception as e:
        logger.error(f"Error processing payment callback: {e}")
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
