import hashlib
import secrets
from django.utils import timezone


def generate_secure_session_id(request):
    """Generate cryptographically secure session ID"""
    entropy_parts = [
        secrets.token_urlsafe(32),
        request.META.get('REMOTE_ADDR', ''),
        request.META.get('HTTP_USER_AGENT', ''),
        str(timezone.now().timestamp()),
    ]

    raw = ''.join(entropy_parts).encode('utf-8')
    return hashlib.sha256(raw).hexdigest()


def validate_session_ownership(session_id, request):
    """Validate that session belongs to current user"""
    from .models import SeatReservation

    existing = SeatReservation.objects.filter(
        session_id=session_id,
        status='reserved'
    ).first()

    if not existing:
        return True

    stored_ip = getattr(existing, 'client_ip', None)
    current_ip = request.META.get('REMOTE_ADDR')

    if stored_ip and stored_ip != current_ip:
        return False

    return True
