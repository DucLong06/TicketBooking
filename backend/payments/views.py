from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404, redirect
from django.db import transaction
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from logzero import logger
from .constant import VNPAY_RESPONSE_CODES

import uuid


from .models import Payment
from .vnpay import VNPay
from bookings.models import Booking


@api_view(['POST'])
def create_payment(request, booking_code):
    """Create payment for booking"""
    booking = get_object_or_404(Booking, booking_code=booking_code)

    if booking.status != 'pending':
        return Response(
            {'error': 'Booking không ở trạng thái chờ thanh toán'},
            status=status.HTTP_400_BAD_REQUEST
        )

    payment_method = request.data.get('payment_method', 'vnpay')

    # Generate transaction ID
    transaction_id = f"TXN{uuid.uuid4().hex[:10].upper()}"

    # Create payment record
    payment = Payment.objects.create(
        booking=booking,
        transaction_id=transaction_id,
        payment_method=payment_method,
        amount=booking.final_amount,
        status='pending'
    )

    if payment_method == 'vnpay':
        vnpay = VNPay()

        # Create VNPay payment URL
        payment_url = vnpay.get_payment_url(
            request=request,
            order_id=transaction_id,
            amount=float(booking.final_amount),
            order_desc=f"Thanh toan ve {booking.booking_code}",
            bank_code=""
        )

        return Response({
            'payment_url': payment_url,
            'transaction_id': transaction_id,
            'amount': float(booking.final_amount),
            'method': 'vnpay'
        })

    else:
        return Response(
            {'error': 'Payment method not supported'},
            status=status.HTTP_400_BAD_REQUEST
        )


@csrf_exempt
@api_view(['GET'])
def vnpay_return(request):
    """Handle VNPay return callback"""
    vnpay = VNPay()

    # Validate response
    if vnpay.validate_response(request.GET):
        transaction_id = request.GET.get('vnp_TxnRef')
        response_code = request.GET.get('vnp_ResponseCode')

        try:
            payment = Payment.objects.get(transaction_id=transaction_id)

            if response_code == '00':  # Success
                with transaction.atomic():
                    # Update payment
                    payment.status = 'success'
                    payment.paid_at = timezone.now()
                    payment.gateway_response = dict(request.GET)
                    payment.gateway_transaction_id = request.GET.get('vnp_TransactionNo')
                    payment.save()

                    # Update booking
                    booking = payment.booking
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
                        logger.debug(f"Failed to send email: {e}")

                # Redirect to success page
                return redirect(f'http://localhost:5173/booking/confirmation/{booking.booking_code}')

            else:  # Failed
                payment.status = 'failed'
                payment.gateway_response = dict(request.GET)
                payment.save()

                error_message = VNPAY_RESPONSE_CODES.get(response_code, f'Lỗi không xác định (Mã lỗi: {response_code})')
                failure_url = f'http://localhost:5173/payment/failed?code={response_code}&message={error_message}'
                return redirect(failure_url)

        except Payment.DoesNotExist:
            return redirect('http://localhost:5173/payment/error')

    else:
        # Invalid signature
        return redirect('http://localhost:5173/payment/error')


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
