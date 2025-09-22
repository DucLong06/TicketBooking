from rest_framework import serializers
from django.utils import timezone
from datetime import timedelta
from .models import Booking, SeatReservation
from venues.models import Seat
from shows.models import Performance


class SeatReservationSerializer(serializers.ModelSerializer):
    seat_label = serializers.CharField(source='seat.full_label', read_only=True)
    row = serializers.CharField(source='seat.row.label', read_only=True)
    number = serializers.IntegerField(source='seat.number', read_only=True)
    section_name = serializers.CharField(source='seat.row.section.name', read_only=True)

    class Meta:
        model = SeatReservation
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


class CreateBookingSerializer(serializers.ModelSerializer):
    seat_ids = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True
    )
    performance_id = serializers.IntegerField(write_only=True)
    session_id = serializers.CharField(write_only=True)

    class Meta:
        model = Booking
        fields = [
            'performance_id', 'seat_ids', 'session_id',
            'customer_name', 'customer_email', 'customer_phone',
            'customer_id_number', 'notes'
        ]

    def validate(self, data):
        performance_id = data.get('performance_id')
        seat_ids = data.get('seat_ids')
        session_id = data.get('session_id')

        # Check if seats are reserved by this session
        reserved_seats = SeatReservation.objects.filter(
            performance_id=performance_id,
            seat_id__in=seat_ids,
            session_id=session_id,
            status='reserved'
        )

        if reserved_seats.count() != len(seat_ids):
            raise serializers.ValidationError("Một số ghế không được giữ bởi phiên này")

        return data

    def create(self, validated_data):
        seat_ids = validated_data.pop('seat_ids')
        performance_id = validated_data.pop('performance_id')
        session_id = validated_data.pop('session_id')

        # Get performance
        performance = Performance.objects.get(id=performance_id)

        # Get seat reservations
        seat_reservations = SeatReservation.objects.filter(
            performance_id=performance_id,
            seat_id__in=seat_ids,
            session_id=session_id,
            status='reserved'
        )

        # Calculate total amount
        total_amount = sum([sr.price for sr in seat_reservations])
        service_fee = len(seat_ids) * 10000  # 10k per ticket
        final_amount = total_amount + service_fee

        # Create booking
        booking = Booking.objects.create(
            performance=performance,
            total_amount=total_amount,
            service_fee=service_fee,
            final_amount=final_amount,
            session_id=session_id,
            **validated_data
        )

        # Update seat reservations
        seat_reservations.update(booking=booking)

        return booking


class BookingDetailSerializer(serializers.ModelSerializer):
    seat_reservations = SeatReservationSerializer(many=True, read_only=True)
    show_name = serializers.CharField(source='performance.show.name', read_only=True)
    performance_datetime = serializers.DateTimeField(source='performance.datetime', read_only=True)
    venue_name = serializers.CharField(source='performance.show.venue.name', read_only=True)

    class Meta:
        model = Booking
        fields = [
            'id', 'booking_code', 'show_name', 'performance_datetime',
            'venue_name', 'customer_name', 'customer_email', 'customer_phone',
            'status', 'total_amount', 'service_fee', 'discount_amount',
            'final_amount', 'seat_reservations', 'created_at', 'expires_at'
        ]
