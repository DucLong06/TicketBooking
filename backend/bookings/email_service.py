from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
import io
import base64


# def generate_qr_code(data):
#     """Generate QR code as base64 string"""
#     qr = qrcode.QRCode(version=1, box_size=10, border=5)
#     qr.add_data(data)
#     qr.make(fit=True)

#     img = qr.make_image(fill_color="black", back_color="white")
#     buffer = io.BytesIO()
#     img.save(buffer, format="PNG")
#     buffer.seek(0)

#     img_str = base64.b64encode(buffer.getvalue()).decode()
#     return f"data:image/png;base64,{img_str}"


def send_booking_confirmation(booking):
    """Send booking confirmation email"""
    try:
        # Generate QR code
        qr_data = {
            'booking_code': booking.booking_code,
            'amount': str(booking.final_amount),
            'performance': booking.performance.id
        }
        # qr_code_img = generate_qr_code(str(qr_data))

        # Prepare context for email template
        context = {
            'booking': booking,
            'show_name': booking.performance.show.name,
            'performance_datetime': booking.performance.datetime,
            'venue_name': booking.performance.show.venue.name,
            'venue_address': booking.performance.show.venue.address,
            'seats': booking.seat_reservations.all(),
            # 'qr_code': qr_code_img,
            'total_amount': booking.final_amount,
            'booking_code': booking.booking_code,
        }

        # Create email content (HTML)
        html_message = f"""
        <html>
        <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <div style="background: #f8f9fa; padding: 20px; border-radius: 10px;">
                <h1 style="color: #333; text-align: center;">Xác Nhận Đặt Vé</h1>
                
                <div style="background: white; padding: 20px; border-radius: 8px; margin: 20px 0;">
                    <h2 style="color: #2563eb;">Thông Tin Vé</h2>
                    <p><strong>Mã đặt vé:</strong> {booking.booking_code}</p>
                    <p><strong>Vở diễn:</strong> {booking.performance.show.name}</p>
                    <p><strong>Ngày diễn:</strong> {booking.performance.datetime.strftime('%d/%m/%Y')}</p>
                    <p><strong>Giờ diễn:</strong> {booking.performance.datetime.strftime('%H:%M')}</p>
                    <p><strong>Địa điểm:</strong> {booking.performance.show.venue.name}</p>
                    <p><strong>Địa chỉ:</strong> {booking.performance.show.venue.address}</p>
                </div>
                
                <div style="background: white; padding: 20px; border-radius: 8px; margin: 20px 0;">
                    <h3 style="color: #2563eb;">Danh Sách Ghế</h3>
                    <ul>
        """

        for seat_reservation in booking.seat_reservations.all():
            html_message += f"""
                        <li>{seat_reservation.seat.row.section.name} - 
                            Hàng {seat_reservation.seat.row.label} - 
                            Ghế {seat_reservation.seat.number} - 
                            {seat_reservation.price:,.0f}đ</li>
            """

        html_message += f"""
                    </ul>
                    <p style="font-size: 18px; font-weight: bold; color: #2563eb;">
                        Tổng cộng: {booking.final_amount:,.0f}đ
                    </p>
                </div>
                
                <div style="background: white; padding: 20px; border-radius: 8px; margin: 20px 0;">
                    <h3 style="color: #2563eb;">Thông Tin Khách Hàng</h3>
                    <p><strong>Họ tên:</strong> {booking.customer_name}</p>
                    <p><strong>Email:</strong> {booking.customer_email}</p>
                    <p><strong>Số điện thoại:</strong> {booking.customer_phone}</p>
                </div>
                
                <div style="background: #fff3cd; padding: 15px; border-radius: 8px; margin: 20px 0;">
                    <h4 style="color: #856404;">Lưu Ý Quan Trọng:</h4>
                    <ul style="color: #856404;">
                        <li>Vui lòng đến trước giờ diễn 30 phút để check-in</li>
                        <li>Mang theo CMND/CCCD khi đến nhận vé</li>
                        <li>Vé đã mua không được hoàn trả hoặc đổi lịch</li>
                    </ul>
                </div>
                
                <div style="text-align: center; margin-top: 30px;">
                    <p style="color: #6c757d;">Cảm ơn bạn đã sử dụng dịch vụ của chúng tôi!</p>
                    <p style="color: #6c757d;">Hồ Gươm Opera</p>
                </div>
            </div>
        </body>
        </html>
        """

        # Plain text version
        text_message = strip_tags(html_message)

        # Send email
        send_mail(
            subject=f'Xác nhận đặt vé - Mã: {booking.booking_code}',
            message=text_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[booking.customer_email],
            html_message=html_message,
            fail_silently=False,
        )

        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False


def send_payment_success(payment):
    """Send payment success notification"""
    booking = payment.booking
    return send_booking_confirmation(booking)
