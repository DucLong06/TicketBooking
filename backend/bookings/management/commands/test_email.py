from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.conf import settings
import time


class Command(BaseCommand):
    help = 'Test email configuration'

    def add_arguments(self, parser):
        parser.add_argument(
            '--to',
            type=str,
            default='test@example.com',
            help='Recipient email address'
        )

    def handle(self, *args, **options):
        recipient = options['to']

        self.stdout.write(self.style.WARNING(f'📧 Testing email to: {recipient}'))
        self.stdout.write(f'Using: {settings.EMAIL_HOST}:{settings.EMAIL_PORT}')
        self.stdout.write(f'From: {settings.EMAIL_HOST_USER}\n')

        start_time = time.time()

        try:
            result = send_mail(
                subject='[TEST] Email từ Django',
                message='Đây là email test từ hệ thống đặt vé Nhà hát Hồ Gươm.',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[recipient],
                fail_silently=False,
            )

            elapsed = time.time() - start_time

            if result == 1:
                self.stdout.write(
                    self.style.SUCCESS(
                        f'✅ Email sent successfully in {elapsed:.2f}s'
                    )
                )
            else:
                self.stdout.write(
                    self.style.ERROR('❌ Email failed to send')
                )

        except Exception as e:
            elapsed = time.time() - start_time
            self.stdout.write(
                self.style.ERROR(
                    f'❌ Error after {elapsed:.2f}s: {str(e)}'
                )
            )
            import traceback
            self.stdout.write(traceback.format_exc())
