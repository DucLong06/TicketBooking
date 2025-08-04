from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from shows.models import Show, Performance, PerformancePrice
from venues.models import Venue, PriceCategory


class Command(BaseCommand):
    help = 'Quickly create a show with performances'

    def add_arguments(self, parser):
        parser.add_argument('name', type=str, help='Show name')
        parser.add_argument('--days', type=int, default=7, help='Number of days to create performances')
        parser.add_argument('--times', type=str, default='19:00,21:00', help='Performance times (comma separated)')

    def handle(self, *args, **options):
        # Get default venue
        venue = Venue.objects.first()
        if not venue:
            self.stdout.write(self.style.ERROR('No venue found. Please create a venue first.'))
            return

        # Create show
        show = Show.objects.create(
            name=options['name'],
            slug=options['name'].lower().replace(' ', '-'),
            category='Hòa nhạc',
            duration_minutes=120,
            description=f"Chương trình {options['name']}",
            venue=venue,
            is_active=True
        )

        self.stdout.write(self.style.SUCCESS(f'Created show: {show.name}'))

        # Create performances
        times = options['times'].split(',')
        start_date = timezone.now().date()

        for day in range(options['days']):
            perf_date = start_date + timedelta(days=day)

            for time_str in times:
                hour, minute = map(int, time_str.split(':'))
                perf_datetime = timezone.make_aware(
                    timezone.datetime.combine(perf_date, timezone.datetime.min.time())
                ).replace(hour=hour, minute=minute)

                # Create performance
                perf = Performance.objects.create(
                    show=show,
                    datetime=perf_datetime,
                    status='on_sale'
                )

                # Auto create prices
                for category in PriceCategory.objects.all():
                    PerformancePrice.objects.create(
                        performance=perf,
                        price_category=category,
                        price=category.base_price
                    )

                self.stdout.write(f'  Created performance: {perf_datetime}')

        self.stdout.write(self.style.SUCCESS('Done!'))
