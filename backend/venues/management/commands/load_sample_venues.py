from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):
    help = 'Load sample venues từ templates'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Ghi đè venues nếu đã tồn tại'
        )

    def handle(self, *args, **options):
        force = options.get('force', False)

        self.stdout.write('Tạo sample venues...')

        self.stdout.write('\n=== Tạo Hồ Gươm Opera ===')
        try:
            call_command(
                'create_venue_from_template',
                '--template=ho_guom_opera',
                '--name=Nhà hát Opera Hồ Gươm',
                '--address=40 Hàng Bài, Hoàn Kiếm, Hà Nội',
                '--phone=024 3825 1999',
                '--email=info@hoguomopera.vn',
                *(['--force'] if force else [])
            )
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Lỗi tạo Hồ Gươm Opera: {e}'))

        self.stdout.write('\n=== Tạo Standard Theater ===')
        try:
            call_command(
                'create_venue_from_template',
                '--template=standard_theater',
                '--name=Rạp hát Thăng Long',
                '--address=123 Nguyễn Huệ, Quận 1, TP.HCM',
                '--phone=028 3829 5555',
                '--email=info@thanglong.theater',
                *(['--force'] if force else [])
            )
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Lỗi tạo Standard Theater: {e}'))

        self.stdout.write(
            self.style.SUCCESS('\nHoàn thành! Các sample venues đã được tạo.')
        )
