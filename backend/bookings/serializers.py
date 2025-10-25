from django.db.models import Q
from logzero import logger
from rest_framework import serializers
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal

from django.conf import settings
from payments.models import Payment
from discounts.models import Discount, DiscountUsage
from discounts.services import validate_and_calculate_discount, DiscountError
from .models import Booking, SeatReservation
from venues.models import Seat
from shows.models import Performance
from django.db import transaction
from django.utils import timezone
import pytz


class SeatReservationSerializer(serializers.ModelSerializer):
    seat = serializers.IntegerField(source='seat.id', read_only=True)
    seat_label = serializers.CharField(source='seat.full_display_label', read_only=True)
    row = serializers.CharField(source='seat.row.label', read_only=True)
    number = serializers.CharField(source='seat.display_label', read_only=True)
    section_name = serializers.CharField(source='seat.row.section.name', read_only=True)

    class Meta:
        model = SeatReservation
        ordering = ['-price']
        fields = [
            'id', 'seat', 'seat_label', 'row', 'number',
            'section_name', 'status', 'price'
        ]


class SeatMapSerializer(serializers.Serializer):
    """Serializer for seat map data"""
    seat_id = serializers.IntegerField()
    row = serializers.CharField()
    number = serializers.IntegerField()
    section_id = serializers.CharField()
    section_name = serializers.CharField()
    position_x = serializers.IntegerField()
    position_y = serializers.IntegerField()
    price = serializers.DecimalField(max_digits=10, decimal_places=0)
    price_category = serializers.CharField()
    status = serializers.CharField()
    is_accessible = serializers.BooleanField()


class ReserveSeatSerializer(serializers.Serializer):
    """Serializer for reserving seats"""
    performance_id = serializers.IntegerField()
    seat_ids = serializers.ListField(
        child=serializers.IntegerField(),
        min_length=1,
        max_length=10
    )
    session_id = serializers.CharField(max_length=100)

    def validate_performance_id(self, value):
        try:
            performance = Performance.objects.get(id=value)
            if performance.status != 'on_sale':
                raise serializers.ValidationError("Suất diễn không mở bán")
            if performance.datetime < timezone.now():
                raise serializers.ValidationError("Suất diễn đã qua")
        except Performance.DoesNotExist:
            raise serializers.ValidationError("Suất diễn không tồn tại")
        return value

    def validate_seat_ids(self, value):
        seats = Seat.objects.filter(id__in=value)
        if seats.count() != len(value):
            raise serializers.ValidationError("Một số ghế không tồn tại")
        return value


class BookingCreateSerializer(serializers.ModelSerializer):
    seat_ids = serializers.ListField(child=serializers.IntegerField(), write_only=True)
    performance_id = serializers.IntegerField(write_only=True)
    session_id = serializers.CharField(write_only=True)
    discount_code = serializers.CharField(required=False, allow_blank=True, write_only=True)

    class Meta:
        model = Booking
        fields = [
            'performance_id', 'seat_ids', 'session_id',
            'customer_name', 'customer_email', 'customer_phone',
            'customer_address', 'shipping_time', 'notes', 'discount_code'
        ]

    def validate(self, data):
        seat_ids = data['seat_ids']
        performance_id = data['performance_id']
        session_id = data['session_id']

        reserved_seats = SeatReservation.objects.filter(
            performance_id=performance_id,
            seat_id__in=seat_ids,
            session_id=session_id,
            status='reserved'
        )

        if reserved_seats.count() != len(seat_ids):
            alternative = SeatReservation.objects.filter(
                performance_id=performance_id,
                seat_id__in=seat_ids,
                status='reserved',
                expires_at__gt=timezone.now(),
                booking__isnull=True
            )
            if alternative.count() == len(seat_ids):
                alternative.update(session_id=session_id)
            else:
                raise serializers.ValidationError(
                    "Ghế không hợp lệ. Vui lòng chọn lại."
                )
        return data

    def create(self, validated_data):
        seat_ids = validated_data.pop('seat_ids')
        performance_id = validated_data.pop('performance_id')
        session_id = validated_data.pop('session_id')
        discount_code_str = validated_data.pop('discount_code', None)

        performance = Performance.objects.select_related('show').get(id=performance_id)

        seat_reservations = SeatReservation.objects.filter(
            performance_id=performance_id,
            seat_id__in=seat_ids,
            session_id=session_id,
            status='reserved',
            expires_at__gt=timezone.now()
        )

        if seat_reservations.count() != len(seat_ids):
            raise serializers.ValidationError({
                "detail": "Ghế không hợp lệ hoặc đã hết hạn. Vui lòng chọn lại.",
                "shouldRedirect": True
            })

        total_amount = sum(sr.price for sr in seat_reservations)
        service_fee = len(seat_ids) * performance.show.service_fee_per_ticket
        shipping_fee = performance.shipping_fee

        if total_amount <= 0:
            raise serializers.ValidationError({
                "detail": "Lỗi tính tiền. Vui lòng thử lại.",
                "shouldRedirect": True
            })

        discount_instance = None
        discount_amount = Decimal('0')

        temp_booking_for_validation = Booking(
            total_amount=total_amount,
            customer_email=validated_data.get('customer_email'),
            customer_phone=validated_data.get('customer_phone'),
            **{k: v for k, v in validated_data.items()
               if k in ['customer_name', 'customer_address', 'shipping_time', 'notes']}
        )

        if discount_code_str:
            try:
                discount_instance, discount_amount = validate_and_calculate_discount(
                    booking=temp_booking_for_validation,
                    code=discount_code_str
                )
            except DiscountError as e:
                raise serializers.ValidationError({'discount_code': str(e)})

        final_amount = total_amount + service_fee + shipping_fee - discount_amount

        with transaction.atomic():
            booking = Booking.objects.create(
                performance=performance,
                session_id=session_id,
                total_amount=total_amount,
                service_fee=service_fee,
                shipping_fee=shipping_fee,
                discount=discount_instance,
                discount_amount=discount_amount,
                final_amount=final_amount,
                **validated_data
            )

            update_count = seat_reservations.update(booking=booking)

            seat_reservations.update(expires_at=booking.expires_at)

            from .models import BookingHistory
            BookingHistory.log_action(
                booking=booking,
                action='create_booking',
                request=self.context.get('request'),
                seats=seat_reservations,
                extra_data={
                    'total_amount': float(total_amount),
                    'service_fee': float(service_fee),
                    'has_discount': bool(discount_instance)
                }
            )

            if update_count != len(seat_ids):
                logger.error(f"🚨 Update mismatch: expected {len(seat_ids)}, got {update_count}")
                raise Exception("CRITICAL: Seat update mismatch")

            if discount_instance:
                DiscountUsage.objects.create(
                    discount=discount_instance,
                    booking=booking,
                    status='PENDING'
                )
                logger.info(f"✅ Created pending discount usage for code '{discount_code_str}'")

        return booking


class BookingDetailSerializer(serializers.ModelSerializer):
    seat_reservations = SeatReservationSerializer(many=True, read_only=True)
    show_name = serializers.CharField(source='performance.show.name', read_only=True)
    performance_datetime = serializers.DateTimeField(source='performance.datetime', read_only=True)
    venue_name = serializers.CharField(source='performance.show.venue.name', read_only=True)
    discount_code = serializers.CharField(source='discount.code', read_only=True, allow_null=True)
    showInfo = serializers.SerializerMethodField()
    performance = serializers.SerializerMethodField()
    customerInfo = serializers.SerializerMethodField()
    selectedSeats = serializers.SerializerMethodField()
    amount = serializers.DecimalField(source='final_amount', max_digits=10, decimal_places=0, read_only=True)
    serviceFee = serializers.DecimalField(source='service_fee', max_digits=10, decimal_places=0, read_only=True)
    ticketAmount = serializers.DecimalField(source='total_amount', max_digits=10, decimal_places=0, read_only=True)
    shippingFee = serializers.DecimalField(source='shipping_fee', max_digits=10, decimal_places=0, read_only=True)

    class Meta:
        model = Booking
        fields = [
            'id', 'booking_code', 'show_name', 'performance_datetime',
            'venue_name', 'customer_name', 'customer_email', 'customer_phone',
            'status', 'total_amount', 'service_fee', 'discount_amount',
            'final_amount', 'seat_reservations', 'created_at', 'expires_at',
            'showInfo', 'performance', 'customerInfo', 'selectedSeats',
            'amount', 'serviceFee', 'ticketAmount', 'discount_code', 'shippingFee'
        ]

    def get_showInfo(self, obj):
        return {'name': obj.performance.show.name}

    def get_performance(self, obj):
        vietnam_tz = pytz.timezone('Asia/Ho_Chi_Minh')
        performance_datetime_vn = obj.performance.datetime.astimezone(vietnam_tz)

        return {
            'date': performance_datetime_vn.strftime('%d/%m/%Y'),
            'time': performance_datetime_vn.strftime('%H:%M')
        }

    def get_customerInfo(self, obj):
        return {
            'fullName': obj.customer_name,
            'email': obj.customer_email,
            'phone': obj.customer_phone,
            'address': obj.customer_address,
            'shippingTime': obj.get_shipping_time_display(),
        }

    def get_selectedSeats(self, obj):
        return [
            {
                'id': sr.seat.id,
                'row': sr.seat.row.label,
                'number': sr.seat.display_label,
                'price': float(sr.price),
                'full_label': sr.seat.full_display_label,
                'section_name': sr.seat.row.section.name,
            }
            for sr in obj.seat_reservations.all()
        ]
