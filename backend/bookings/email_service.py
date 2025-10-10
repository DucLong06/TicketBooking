from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from datetime import timedelta
from logzero import logger
from venues.models import ContactInfo


def send_booking_confirmation(booking):
    """Send booking confirmation email using template"""
    try:
        # Get contact information
        contact = ContactInfo.get_instance()

        # Get booking details
        show = booking.performance.show
        venue = show.venue
        performance = booking.performance

        # Format seat numbers
        seats = booking.seat_reservations.all()

        # Group seats by section for better readability
        from collections import defaultdict
        seats_by_section = defaultdict(list)

        for reservation in seats:
            seat = reservation.seat
            section_name = seat.row.section.name
            seat_label = f"{seat.row.label}{seat.display_label}"
            seats_by_section[section_name].append(seat_label)

        # Format: "Khán Phòng 1: A1, A2, B3 | Khán Phòng 2: C1, C2"
        seat_numbers = " | ".join([
            f"{section}: {', '.join(seats)}"
            for section, seats in seats_by_section.items()
        ])

        # Get ticket class from first seat
        ticket_class = ""  # Default
        if seats.exists():
            first_seat = seats.first()
            ticket_class = first_seat.seat.row.price_category.name

        # Calculate check-in time
        checkin_minutes = getattr(venue, 'checkin_minutes_before', 45)
        checkin_time = performance.datetime - timedelta(minutes=checkin_minutes)
        checkin_time_str = f"{checkin_time.strftime('%H:%M')} ngày {checkin_time.strftime('%d/%m/%Y')}"

        # Format performance datetime for display and calendar
        performance_datetime_display = f"{performance.datetime.strftime('%H')}h - {performance.datetime.strftime('%d/%m/%Y')}"

        # Calendar format for Google Calendar link
        performance_datetime_cal = performance.datetime.strftime('%Y%m%dT%H%M00Z')
        performance_end_cal = (performance.datetime + timedelta(minutes=show.duration_minutes)
                               ).strftime('%Y%m%dT%H%M00Z')

        # Determine payment status section
        payment_section = ""
        payment_status = getattr(booking, 'payment_status', 'pending')

        if payment_status == 'cod':
            payment_section = """
            <tr>
                <td class="banve" style="width: 30%; font-weight: bold;">
                    Tình trạng thanh toán <br>
                    <span style="font-style: italic; font-weight: normal;">Payment Status</span>
                </td>
                <td class="banve" style="">
                    <a style="font-weight: bold; color: #6d4c41;">Thanh toán khi nhận vé.</a>
              <br>
              <span style="font-style: italic; font-weight: normal;">Cash on delivery.</span>
                      </td>
                  </tr>
            """
        elif payment_status == 'completed':
            payment_section = """
            <tr>
                <td class="banve" style="width: 30%; font-weight: bold;">
                    Tình trạng <br> 
                    <span style="font-style: italic; font-weight: normal;">Status</span>
                </td>
                <td class="banve" style=" font-weight: bold; color: #6d4c41; text-transform: uppercase">Đã thanh toán</td>
            </tr>
            """
        else:
            payment_section = """
            <tr>
                <td class="banve" style="width: 30%; font-weight: bold;">
                    Tình trạng <br> 
                    <span style="font-style: italic; font-weight: normal;">Status</span>
                </td>
                <td class="banve" style=" font-weight: bold; color: #6d4c41; text-transform: uppercase">Vé mới</td>
            </tr>
            """

        # Template context
        context = {
            'customer_name': booking.customer_name,
            'phone': booking.customer_phone,
            'address': getattr(booking, 'customer_address', 'Hà Nội, Việt Nam'),
            'booking_code': booking.booking_code,
            'ticket_count': seats.count(),
            'ticket_class': ticket_class,
            'seat_numbers': seat_numbers,
            'total_amount': f"{booking.final_amount:,.0f}",
            'show': show,
            'venue': venue,
            'performance_datetime_display': performance_datetime_display,
            'performance_datetime_cal': f"{performance_datetime_cal}/{performance_end_cal}",
            'venue_maps_url': venue.maps_url,
            'checkin_time': checkin_time_str,
            'payment_section': payment_section,
            'contact': contact,
            'logo_url': contact.logo_url,
            'header_text': 'XÁC NHẬN ĐẶT VÉ THÀNH CÔNG',
        }

        # Render HTML email
        html_message = render_to_string('emails/booking_confirmation.html', context)

        # Plain text version
        text_message = strip_tags(html_message)

        # Send email
        send_mail(
            subject=f'Xác nhận đặt vé {show.name} - Mã: {booking.booking_code}',
            message=text_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[booking.customer_email],
            html_message=html_message,
            fail_silently=False,
        )

        logger.info(f"Email sent successfully to {booking.customer_email}")
        return True

    except Exception as e:
        logger.error(f"Error sending email: {e}")
        return False


def send_payment_success(payment):
    """Send payment success notification"""
    booking = payment.booking
    # Update payment status
    booking.payment_status = 'completed'
    booking.save()
    return send_booking_confirmation(booking)
