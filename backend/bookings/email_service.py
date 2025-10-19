from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from datetime import timedelta
from logzero import logger
from venues.models import ContactInfo
from django.utils import timezone
import pytz


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

        section_names = list(seats_by_section.keys())
        if len(section_names) == 1:
            section_display_name = section_names[0]
        elif len(section_names) > 1:
            section_display_name = ', '.join(section_names)
        else:
            section_display_name = venue.name

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
        vietnam_tz = pytz.timezone('Asia/Ho_Chi_Minh')
        performance_datetime_vn = performance.datetime.astimezone(vietnam_tz)
        checkin_minutes = getattr(venue, 'checkin_minutes_before', 45)
        checkin_time = performance_datetime_vn - timedelta(minutes=checkin_minutes)
        checkin_time_str = f"{checkin_time.strftime('%H:%M')} ngày {checkin_time.strftime('%d/%m/%Y')}"

        # Format performance datetime for display and calendar
        performance_datetime_display = f"{performance_datetime_vn.strftime('%H')}h - {performance_datetime_vn.strftime('%d/%m/%Y')}"

        # Calendar format for Google Calendar link
        performance_datetime_cal = performance_datetime_vn.strftime('%Y%m%dT%H%M00')
        performance_end = performance_datetime_vn + timedelta(minutes=show.duration_minutes)
        performance_end_cal = performance_end.strftime('%Y%m%dT%H%M00')

        # Determine payment status section
        payment_section = ""

        payment_section = """
            <tr>
                <td class="banve" style="width: 30%; font-weight: bold;">
                    Tình trạng <br> 
                    <span style="font-style: italic; font-weight: normal;">Status</span>
                </td>
                <td class="banve" style=" font-weight: bold; color: #6d4c41; text-transform: uppercase">Đã thanh toán</td>
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
            'section_name': section_display_name,
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
