
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = ''

    def add_arguments(self, parser):
        parser.add_argument(
            '--create-user',
            action='store_true',
            help='',
        )

    def handle(self, *args, **options):
        self.stdout.write('=' * 60)
        self.stdout.write(self.style.SUCCESS('create gr ke toan'))
        self.stdout.write('=' * 60)

        # Setup group
        self.setup_ketoan_group()

        # Create sample user if requested

        # Show permissions
        self.show_permissions()

        self.stdout.write('')
        self.stdout.write('=' * 60)
        self.stdout.write(self.style.SUCCESS('✅ HOÀN TẤT!'))
        self.stdout.write('=' * 60)

    def setup_ketoan_group(self):
        group, created = Group.objects.get_or_create(name='Kế toán')

        if created:
            self.stdout.write(self.style.SUCCESS("Đã tạo group 'Kế toán'"))
        else:
            self.stdout.write(self.style.WARNING("Group 'Kế toán' đã tồn tại, đang cập nhật permissions..."))
            group.permissions.clear()

        models_to_grant = [
            ('bookings', 'booking'),
            ('bookings', 'seatreservation'),
            ('bookings', 'bookinghistory'),
        ]

        permissions_added = []

        for app_label, model_name in models_to_grant:
            try:
                content_type = ContentType.objects.get(app_label=app_label, model=model_name)
                perm_codename = f'view_{model_name}'
                permission = Permission.objects.get(
                    codename=perm_codename,
                    content_type=content_type
                )

                group.permissions.add(permission)
                permissions_added.append(f"{app_label}.{perm_codename}")
                self.stdout.write(f"  ✓ Đã cấp quyền: {perm_codename}")

            except ContentType.DoesNotExist:
                self.stdout.write(self.style.ERROR(f"Không tìm thấy ContentType cho {app_label}.{model_name}"))
            except Permission.DoesNotExist:
                self.stdout.write(self.style.ERROR(f"Không tìm thấy permission {perm_codename}"))

        self.stdout.write(self.style.SUCCESS(f"\nĐã cấu hình {len(permissions_added)} permissions"))

    def show_permissions(self):
        try:
            group = Group.objects.get(name='Kế toán')
            permissions = group.permissions.all()

            self.stdout.write('\n📋 Permissions của group "Kế toán":')
            for perm in permissions:
                self.stdout.write(f"   - {perm.content_type.app_label}.{perm.codename}: {perm.name}")
        except Group.DoesNotExist:
            self.stdout.write(self.style.ERROR("\n⚠️  Group 'Kế toán' chưa tồn tại"))
