from celery import shared_task
from django.utils import timezone
from django.db import transaction
from django.conf import settings
from datetime import timedelta
import logging

from .models import SeatReservation, Booking
from discounts.models import DiscountUsage
from payments.models import Payment
from payments.ninepay import NinePay
from .email_service import send_booking_confirmation

logger = logging.getLogger(__name__)


@shared_task
def cleanup_expired_seat_reservations():
    now = timezone.now()

    expired_reservations = SeatReservation.objects.filter(
        status='reserved',
        expires_at__lt=now
    ).select_related('booking')

    count = 0

    for reservation in expired_reservations:
        if not reservation.booking:
            reservation.status = 'available'
            reservation.session_id = ''
            reservation.expires_at = None
            reservation.booking = None
            reservation.client_ip = None
            reservation.save()
            count += 1

        elif reservation.booking.status in ['cancelled', 'expired']:
            reservation.status = 'available'
            reservation.session_id = ''
            reservation.expires_at = None
            reservation.booking = None
            reservation.client_ip = None
            reservation.save()
            count += 1

    if count > 0:
        logger.info(f"✅ [Celery] Cleaned {count} expired seat reservations")

    return {
        'task': 'cleanup_expired_seat_reservations',
        'cleaned': count,
        'timestamp': now.isoformat()
    }


@shared_task
def expire_old_pending_bookings():
    now = timezone.now()

    payment_timeout = getattr(settings, 'PAYMENT_TIMEOUT_MINUTES', 30)
    buffer_minutes = getattr(settings, 'BOOKING_EXPIRATION_BUFFER_MINUTES', 2)
    total_timeout = payment_timeout + buffer_minutes

    cutoff_time = now - timedelta(minutes=total_timeout)

    logger.info(f"[Celery] expire_old_pending_bookings - Cutoff: {cutoff_time.isoformat()}")

    old_bookings = Booking.objects.filter(
        status='pending',
        created_at__lt=cutoff_time
    ).prefetch_related('seat_reservations')

    if not old_bookings.exists():
        return {
            'task': 'expire_old_pending_bookings',
            'expired': 0,
            'timestamp': now.isoformat()
        }

    expired_count = 0
    skipped_count = 0

    for booking in old_bookings:
        try:
            has_pending_payment = Payment.objects.filter(
                booking=booking,
                status='pending'
            ).exists()

            if has_pending_payment:
                logger.info(
                    f"⏳ [Celery] Skip booking {booking.booking_code} - "
                    f"Has pending payment, let sync_9pay handle it"
                )
                skipped_count += 1
                continue

            with transaction.atomic():
                booking.status = 'expired'
                booking.save()

                # Release seats
                booking.seat_reservations.update(
                    status='available',
                    session_id='',
                    expires_at=None,
                    booking=None
                )

                # Cancel discount
                try:
                    usage = DiscountUsage.objects.get(
                        booking=booking,
                        status='PENDING'
                    )
                    usage.status = 'CANCELLED'
                    usage.save()
                except DiscountUsage.DoesNotExist:
                    pass

                expired_count += 1
                logger.info(f"✅ [Celery] Expired booking {booking.booking_code}")

        except Exception as e:
            logger.error(f"❌ [Celery] Error expiring booking {booking.booking_code}: {e}")

    logger.info(
        f"✅ [Celery] expire_old_pending_bookings - "
        f"Expired: {expired_count}, Skipped: {skipped_count}"
    )

    return {
        'task': 'expire_old_pending_bookings',
        'expired': expired_count,
        'skipped': skipped_count,
        'timestamp': now.isoformat()
    }


@shared_task
def sync_pending_payments_with_9pay():
    now = timezone.now()

    min_age = timedelta(minutes=settings.SEAT_RESERVATION_TIMEOUT_MINUTES)

    cutoff_max = now - min_age

    logger.info(
        f"[Celery] sync_pending_payments - "
    )

    pending_payments = Payment.objects.filter(
        status='pending',
        created_at__lte=cutoff_max
    ).select_related('booking')

    if not pending_payments.exists():
        return {
            'task': 'sync_pending_payments_with_9pay',
            'checked': 0,
            'timestamp': now.isoformat()
        }

    logger.info(f"[Celery] Found {pending_payments.count()} pending payments to check")

    ninepay = NinePay()

    success_count = 0
    failed_count = 0
    no_change_count = 0

    for payment in pending_payments:
        try:
            result = ninepay.query_payment_status(payment.transaction_id)

            if not result['success']:
                logger.warning(
                    f"⚠️ [Celery] Cannot query 9Pay for {payment.transaction_id}: "
                    f"{result.get('message')}"
                )
                continue

            status = result['status']
            error_code = result['error_code']
            data = result['data']

            if status == 5 and error_code == '000':
                logger.info(f"💰 [Celery] Payment {payment.transaction_id} is SUCCESSFUL")
                update_payment_success(payment, data)
                success_count += 1

            elif status in [6, 8]:
                logger.warning(f"❌ [Celery] Payment {payment.transaction_id} FAILED/CANCELLED")
                update_payment_failed(payment, data)
                failed_count += 1

            elif status in [2, 3]:
                logger.info(f"⏳ [Celery] Payment {payment.transaction_id} still processing")
                no_change_count += 1

            else:
                logger.warning(
                    f"⚠️ [Celery] Payment {payment.transaction_id} - "
                    f"Unknown status: {status}"
                )
                no_change_count += 1

        except Exception as e:
            logger.error(
                f"❌ [Celery] Error syncing payment {payment.transaction_id}: {e}",
                exc_info=True
            )

    logger.info(
        f"✅ [Celery] sync_pending_payments - "
        f"Success: {success_count}, Failed: {failed_count}, "
        f"No change: {no_change_count}"
    )

    return {
        'task': 'sync_pending_payments_with_9pay',
        'checked': pending_payments.count(),
        'success': success_count,
        'failed': failed_count,
        'no_change': no_change_count,
        'timestamp': now.isoformat()
    }


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def update_payment_success(payment, gateway_response):
    try:
        with transaction.atomic():
            payment = Payment.objects.select_for_update().get(id=payment.id)
            booking = Booking.objects.select_for_update().get(id=payment.booking_id)

            if payment.status != 'pending':
                logger.warning(
                    f"⚠️ [Celery] Payment {payment.transaction_id} "
                    f"already processed: {payment.status}"
                )
                return False

            if booking.status != 'pending':
                logger.error(
                    f"🚨 [Celery] Booking {booking.booking_code} "
                    f"not pending: {booking.status}"
                )
                return False

            seat_ids = booking.seat_reservations.values_list('seat_id', flat=True)

            duplicate_seats = SeatReservation.objects.filter(
                seat_id__in=seat_ids,
                performance=booking.performance,
                status='sold'
            ).exclude(booking=booking)

            if duplicate_seats.exists():
                logger.error(
                    f"🚨🚨🚨 [Celery] CRITICAL: SEAT CONFLICT for booking {booking.booking_code}!\n"
                    f"Seats {list(duplicate_seats.values_list('seat_id', flat=True))} "
                    f"already sold to another booking!"
                )

                payment.status = 'failed'
                payment.gateway_response = {
                    'error': 'SEAT_CONFLICT',
                    'message': 'Seats already sold to another booking',
                    'original_response': gateway_response
                }
                payment.save()

                booking.status = 'cancelled'
                booking.save()

                return False

            payment.status = 'success'
            payment.paid_at = timezone.now()
            payment.gateway_response = gateway_response
            payment.gateway_transaction_id = gateway_response.get('payment_no')
            payment.save()

            # ✅ Update booking
            booking.status = 'paid'
            booking.paid_at = timezone.now()
            booking.session_id = ''  # Clear session
            booking.save()

            # ✅ Update seats
            updated_seats = booking.seat_reservations.update(status='sold')
            logger.info(f"✅ [Celery] Updated {updated_seats} seats to 'sold'")

            # ✅ Confirm discount
            try:
                usage = DiscountUsage.objects.get(booking=booking, status='PENDING')
                usage.status = 'COMPLETED'
                usage.save()

                discount = usage.discount
                discount.usage_count += 1
                discount.save()

                logger.info(f"✅ [Celery] Confirmed discount usage")
            except DiscountUsage.DoesNotExist:
                pass

            # ✅ Send email async
            send_confirmation_email_async.delay(booking.id)

            logger.info(
                f"✅✅✅ [Celery] Payment {payment.transaction_id} "
                f"synced successfully for booking {booking.booking_code}"
            )

            return True

    except Exception as e:
        logger.error(f"❌ [Celery] Error in update_payment_success: {e}", exc_info=True)
        return False


def update_payment_failed(payment, gateway_response):
    """Update payment failed"""
    try:
        with transaction.atomic():
            payment = Payment.objects.select_for_update().get(id=payment.id)
            booking = Booking.objects.select_for_update().get(id=payment.booking_id)

            if payment.status != 'pending':
                logger.warning(f"⚠️ [Celery] Payment already processed: {payment.status}")
                return False

            # Update payment
            payment.status = 'failed'
            payment.gateway_response = gateway_response
            payment.save()

            # Cancel booking
            booking.status = 'cancelled'
            booking.save()

            # Release seats
            booking.seat_reservations.update(
                status='available',
                session_id='',
                expires_at=None,
                booking=None
            )

            # Cancel discount
            try:
                usage = DiscountUsage.objects.get(booking=booking, status='PENDING')
                usage.status = 'CANCELLED'
                usage.save()
            except DiscountUsage.DoesNotExist:
                pass

            logger.info(f"❌ [Celery] Payment {payment.transaction_id} marked as failed")
            return True

    except Exception as e:
        logger.error(f"❌ [Celery] Error in update_payment_failed: {e}", exc_info=True)
        return False


# ============================================================================
# TASK 4: Send Email Async
# ============================================================================

@shared_task(bind=True, max_retries=3)
def send_confirmation_email_async(self, booking_id):
    """Gửi email async với retry"""
    try:
        booking = Booking.objects.get(id=booking_id)
        success = send_booking_confirmation(booking)

        if success:
            logger.info(f"✅ [Celery] Email sent for booking {booking.booking_code}")
        else:
            raise Exception("Email sending returned False")

    except Booking.DoesNotExist:
        logger.error(f"❌ [Celery] Booking {booking_id} not found")
        return False

    except Exception as e:
        logger.error(f"❌ [Celery] Email error: {e}")
        raise self.retry(exc=e, countdown=300)  # Retry after 5 min
