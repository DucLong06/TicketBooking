from celery import Celery
from celery.schedules import crontab
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

app = Celery('ticket_booking')
app.config_from_object('django.conf:settings', namespace='CELERY')


app.conf.beat_schedule = {
    'cleanup-expired-seat-reservations': {
        'task': 'bookings.tasks.cleanup_expired_seat_reservations',
        'schedule': crontab(minute='*'),
    },
    'sync-pending-payments-with-9pay': {
        'task': 'bookings.tasks.sync_pending_payments_with_9pay',
        'schedule': crontab(minute='*/2'),
    },
    'expire-old-pending-bookings': {
        'task': 'bookings.tasks.expire_old_pending_bookings',
        'schedule': crontab(minute='1-59/2'),
    },
}
app.autodiscover_tasks()


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
