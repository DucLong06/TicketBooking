from rest_framework import serializers
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal

from discounts.models import Discount, DiscountUsage
from discounts.services import validate_and_calculate_discount, DiscountError
from .models import Booking, SeatReservation
from venues.models import Seat
from shows.models import Performance


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
        max_length=8
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
            status='reserved'
        )

        if seat_reservations.count() == 0:
            raise serializers.ValidationError(
                "Không tìm thấy ghế. Vui lòng chọn lại."
            )

        total_amount = sum(sr.price for sr in seat_reservations)
        service_fee = len(seat_ids) * performance.show.service_fee_per_ticket

        discount_instance = None
        discount_amount = Decimal('0')

        # Create a temporary booking object to pass to the service
        temp_booking_for_validation = Booking(
            total_amount=total_amount,
            **validated_data
        )

        if discount_code_str:
            try:
                discount_instance, discount_amount = validate_and_calculate_discount(
                    booking=temp_booking_for_validation,
                    code=discount_code_str
                )
            except DiscountError as e:
                raise serializers.ValidationError({'discount_code': str(e)})

        final_amount = total_amount + service_fee - discount_amount

        # Delete old pending bookings from the same session to avoid duplicates
        Booking.objects.filter(session_id=session_id, status='pending').delete()

        # Create the new booking with all correctly calculated data
        booking = Booking.objects.create(
            performance=performance,
            session_id=session_id,
            total_amount=total_amount,
            service_fee=service_fee,
            discount=discount_instance,
            discount_amount=discount_amount,
            final_amount=final_amount,
            **validated_data
        )

        seat_reservations.update(booking=booking)

        if booking.seat_reservations.count() != len(seat_ids):
            booking.delete()
            raise serializers.ValidationError("Lỗi hệ thống. Vui lòng thử lại.")

        if discount_instance:
            DiscountUsage.objects.create(discount=discount_instance, booking=booking, status='PENDING')

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

    class Meta:
        model = Booking
        fields = [
            'id', 'booking_code', 'show_name', 'performance_datetime',
            'venue_name', 'customer_name', 'customer_email', 'customer_phone',
            'status', 'total_amount', 'service_fee', 'discount_amount',
            'final_amount', 'seat_reservations', 'created_at', 'expires_at',
            'showInfo', 'performance', 'customerInfo', 'selectedSeats',
            'amount', 'serviceFee', 'ticketAmount', 'discount_code',
        ]

    def get_showInfo(self, obj):
        return {'name': obj.performance.show.name}

    def get_performance(self, obj):
        return {
            'date': obj.performance.datetime.strftime('%d/%m/%Y'),
            'time': obj.performance.datetime.strftime('%H:%M')
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
