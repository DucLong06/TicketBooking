from django.db import models
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Discount
from django.utils import timezone


@api_view(['GET'])
def get_available_discounts(request):
    """
    Get available discount codes based on ticket quantity
    Query params:
    - ticket_count: number of tickets
    - email: customer email (optional)
    - phone: customer phone (optional)
    """
    ticket_count = int(request.GET.get('ticket_count', 0))
    email = request.GET.get('email', '')
    phone = request.GET.get('phone', '')

    now = timezone.now()

    # Base queryset: active, not expired, has usage left
    discounts = Discount.objects.filter(
        is_active=True,
        valid_from__lte=now,
    ).filter(
        models.Q(valid_to__isnull=True) | models.Q(valid_to__gte=now)
    ).filter(
        models.Q(max_usage__isnull=True) | models.Q(usage_count__lt=models.F('max_usage'))
    )

    # Filter by ticket quantity
    if ticket_count > 0:
        discounts = discounts.filter(
            models.Q(min_ticket_quantity__isnull=True) |
            models.Q(min_ticket_quantity__lte=ticket_count)
        )

    # Filter by user eligibility
    eligible_discounts = []
    for discount in discounts:
        is_valid, _ = discount.is_valid(user_email=email, user_phone=phone)
        if is_valid:
            eligible_discounts.append({
                'code': discount.code,
                'description': str(discount),
                'min_ticket_quantity': discount.min_ticket_quantity,
                'discount_type': discount.discount_type,
                'value': float(discount.value)
            })

    return Response({'discounts': eligible_discounts})
