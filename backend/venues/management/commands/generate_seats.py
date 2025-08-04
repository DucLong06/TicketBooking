from venues.models import Venue, Section, Row, Seat, PriceCategory
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Generate seats for a venue'

    def handle(self, *args, **options):
        # Create price categories
        vip, _ = PriceCategory.objects.get_or_create(
            code='vip',
            defaults={'name': 'VIP', 'base_price': 2000000, 'color': '#FFD700'}
        )
        standard, _ = PriceCategory.objects.get_or_create(
            code='standard',
            defaults={'name': 'Standard', 'base_price': 1200000, 'color': '#87CEEB'}
        )
        economy, _ = PriceCategory.objects.get_or_create(
            code='economy',
            defaults={'name': 'Economy', 'base_price': 800000, 'color': '#90EE90'}
        )

        # Get or create venue
        venue, created = Venue.objects.get_or_create(
            name='Hồ Gươm Opera',
            defaults={
                'address': '40 Hàng Bài, Hà Nội',
                'phone': '0835661999',
                'email': 'contact@hoguomopera.com'
            }
        )

        if created:
            self.stdout.write(self.style.SUCCESS(f'Created venue: {venue.name}'))

        # Create sections and seats
        # Section A - VIP
        section_a, _ = Section.objects.get_or_create(
            venue=venue,
            code='section-a',
            defaults={'name': 'Khu A - VIP', 'position_x': 200, 'position_y': 280, 'order': 1}
        )

        # Create rows for Section A
        for i, row_label in enumerate(['A', 'B', 'C', 'D']):
            row, _ = Row.objects.get_or_create(
                section=section_a,
                label=row_label,
                defaults={
                    'seat_count': 18 + i * 2,  # A:18, B:20, C:22, D:22
                    'position_y': 280 + i * 35,
                    'price_category': vip
                }
            )

            # Create seats for this row
            for seat_num in range(1, row.seat_count + 1):
                seat, created = Seat.objects.get_or_create(
                    row=row,
                    number=seat_num,
                    defaults={
                        'position_x': 200 + (seat_num - 1) * 22,
                        'position_y': row.position_y
                    }
                )
                if created:
                    self.stdout.write(f'Created seat {row.label}{seat_num}')

        self.stdout.write(self.style.SUCCESS('Successfully generated seats'))
