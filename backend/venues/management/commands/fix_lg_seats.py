from django.core.management.base import BaseCommand
from venues.models import Row, Seat
from django.db import transaction


class Command(BaseCommand):
    help = 'Fix LG seats position_y for vertical layout'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be done without making changes',
        )
        parser.add_argument(
            '--strategy',
            type=str,
            choices=['recreate', 'update', 'create-only'],
            default='recreate',
            help='Strategy: recreate (delete+create), update (modify existing), create-only (skip if exists)',
        )
        parser.add_argument(
            '--venue',
            type=str,
            help='Filter by venue name (e.g., "Hồ Gươm")',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        strategy = options['strategy']
        venue_filter = options.get('venue')

        self.stdout.write(self.style.WARNING('=' * 70))
        self.stdout.write(self.style.WARNING('FIX LG SEATS - VERTICAL POSITIONING'))
        self.stdout.write(self.style.WARNING('=' * 70))

        if dry_run:
            self.stdout.write(self.style.NOTICE(f'🔍 DRY RUN MODE - No changes will be made'))

        self.stdout.write(self.style.NOTICE(f'📋 Strategy: {strategy.upper()}\n'))

        # Find all LG rows
        lg_rows = Row.objects.filter(label='LG').select_related('section', 'section__venue')

        if venue_filter:
            lg_rows = lg_rows.filter(section__venue__name__icontains=venue_filter)
            self.stdout.write(self.style.NOTICE(f'🔍 Filtering by venue: {venue_filter}'))

        if not lg_rows.exists():
            self.stdout.write(self.style.ERROR('❌ No LG rows found!'))
            return

        self.stdout.write(self.style.SUCCESS(f'✅ Found {lg_rows.count()} LG rows\n'))

        total_created = 0
        total_updated = 0
        total_deleted = 0

        for row in lg_rows:
            self.stdout.write(self.style.WARNING(f'\n{"=" * 70}'))
            self.stdout.write(self.style.WARNING(
                f'📍 Processing: {row.section.venue.name} - {row.section.name} - {row.label}'))
            self.stdout.write(f'   Row position_y: {row.position_y}')
            self.stdout.write(f'   Numbering style: {row.numbering_style}')
            self.stdout.write(f'   Expected seats: {row.seat_count}')

            current_seats = row.seats.all().order_by('number')
            self.stdout.write(f'   Current seats in DB: {current_seats.count()}')

            # Show current state
            if current_seats.exists():
                self.stdout.write(f'\n   Current seats:')
                for seat in current_seats[:5]:
                    status = '✅' if seat.position_y > 0 else '❌'
                    self.stdout.write(f'      {status} Seat {seat.number}: position_y={seat.position_y}')
                if current_seats.count() > 5:
                    self.stdout.write(f'      ... and {current_seats.count() - 5} more')
            else:
                self.stdout.write(self.style.NOTICE('   ℹ️  No seats exist yet'))

            # Execute strategy
            if dry_run:
                self._dry_run_preview(row, strategy, current_seats)
                continue

            try:
                with transaction.atomic():
                    if strategy == 'recreate':
                        created, updated, deleted = self._strategy_recreate(row, current_seats)
                    elif strategy == 'update':
                        created, updated, deleted = self._strategy_update(row, current_seats)
                    else:  # create-only
                        created, updated, deleted = self._strategy_create_only(row, current_seats)

                    total_created += created
                    total_updated += updated
                    total_deleted += deleted

            except Exception as e:
                self.stdout.write(self.style.ERROR(f'\n   ❌ ERROR: {str(e)}'))
                continue

        # Summary
        self.stdout.write(self.style.WARNING('\n' + '=' * 70))
        self.stdout.write(self.style.WARNING('SUMMARY'))
        self.stdout.write(self.style.WARNING('=' * 70))

        if dry_run:
            self.stdout.write(self.style.NOTICE('🔍 DRY RUN COMPLETED - Run without --dry-run to apply changes'))
        else:
            self.stdout.write(self.style.SUCCESS(f'✅ Created: {total_created} seats'))
            self.stdout.write(self.style.SUCCESS(f'✅ Updated: {total_updated} seats'))
            if total_deleted > 0:
                self.stdout.write(self.style.WARNING(f'⚠️  Deleted: {total_deleted} seats'))
            self.stdout.write(self.style.WARNING('\n⚠️  Remember to restart your web server!'))
            self.stdout.write(self.style.NOTICE('\nRestart commands:'))
            self.stdout.write('   sudo systemctl restart gunicorn')
            self.stdout.write('   # or')
            self.stdout.write('   sudo systemctl restart uwsgi')

        self.stdout.write(self.style.WARNING('=' * 70))

    def _dry_run_preview(self, row, strategy, current_seats):
        """Show what would happen without making changes"""
        self.stdout.write(self.style.NOTICE(f'\n   Would execute strategy: {strategy}'))

        if strategy == 'recreate':
            self.stdout.write(f'      1. Update row: numbering_style=vertical, position_y=390')
            self.stdout.write(f'      2. Delete {current_seats.count()} existing seats')
            self.stdout.write(f'      3. Create {row.seat_count} new seats with correct position_y')

        elif strategy == 'update':
            if not current_seats.exists():
                self.stdout.write(f'      1. Update row: numbering_style=vertical, position_y=390')
                self.stdout.write(f'      2. Create {row.seat_count} new seats')
            else:
                self.stdout.write(f'      1. Update row: numbering_style=vertical, position_y=390')
                self.stdout.write(f'      2. Update position_y for {current_seats.count()} existing seats')
                if current_seats.count() < row.seat_count:
                    missing = row.seat_count - current_seats.count()
                    self.stdout.write(f'      3. Create {missing} missing seats')
                elif current_seats.count() > row.seat_count:
                    extra = current_seats.count() - row.seat_count
                    self.stdout.write(self.style.WARNING(f'      3. Delete {extra} extra seats'))

        else:  # create-only
            if current_seats.exists():
                self.stdout.write(self.style.NOTICE('      Skip - seats already exist'))
            else:
                self.stdout.write(f'      1. Update row: numbering_style=vertical, position_y=390')
                self.stdout.write(f'      2. Create {row.seat_count} new seats')

    def _strategy_recreate(self, row, current_seats):
        """Delete all and recreate - SAFEST"""
        self.stdout.write(self.style.WARNING('\n   Executing RECREATE strategy...'))

        # Update row
        row.numbering_style = 'vertical'
        row.position_y = 390
        row.save()
        self.stdout.write(self.style.SUCCESS('   ✅ Row updated'))

        # Delete old seats
        deleted = current_seats.count()
        if deleted > 0:
            current_seats.delete()
            self.stdout.write(self.style.SUCCESS(f'   ✅ Deleted {deleted} old seats'))

        # Create new seats
        created = row.create_default_seats()
        self.stdout.write(self.style.SUCCESS(f'   ✅ Created {created} new seats'))

        # Verify
        self._verify_seats(row)

        return created, 0, deleted

    def _strategy_update(self, row, current_seats):
        """Update existing seats or create if missing"""
        self.stdout.write(self.style.WARNING('\n   Executing UPDATE strategy...'))

        # Update row
        row.numbering_style = 'vertical'
        row.position_y = 390
        row.save()
        self.stdout.write(self.style.SUCCESS('   ✅ Row updated'))

        created = 0
        updated = 0
        deleted = 0

        if not current_seats.exists():
            # No seats exist, create them
            created = row.create_default_seats()
            self.stdout.write(self.style.SUCCESS(f'   ✅ Created {created} new seats'))
        else:
            # Calculate positions
            positions = row.actual_seat_positions

            # Update existing seats
            for seat in current_seats:
                seat_num = int(seat.number)
                if seat_num in positions:
                    new_pos = positions[seat_num]
                    if seat.position_x != new_pos['x'] or seat.position_y != new_pos['y']:
                        seat.position_x = new_pos['x']
                        seat.position_y = new_pos['y']
                        seat.save()
                        updated += 1

            self.stdout.write(self.style.SUCCESS(f'   ✅ Updated {updated} seats'))

            # Check for missing seats
            existing_numbers = set(int(s.number) for s in current_seats)
            expected_numbers = set(range(1, row.seat_count + 1))
            missing_numbers = expected_numbers - existing_numbers

            if missing_numbers:
                self.stdout.write(self.style.WARNING(f'   ⚠️  Creating {len(missing_numbers)} missing seats'))
                for num in sorted(missing_numbers):
                    if num in positions:
                        pos = positions[num]
                        Seat.objects.create(
                            row=row,
                            number=str(num),
                            display_number=str(num),
                            position_x=pos['x'],
                            position_y=pos['y'],
                            price_category=row.price_category,
                            status='active'
                        )
                        created += 1
                self.stdout.write(self.style.SUCCESS(f'   ✅ Created {created} missing seats'))

            # Check for extra seats
            extra_numbers = existing_numbers - expected_numbers
            if extra_numbers:
                self.stdout.write(self.style.WARNING(f'   ⚠️  Deleting {len(extra_numbers)} extra seats'))
                Seat.objects.filter(row=row, number__in=[str(n) for n in extra_numbers]).delete()
                deleted = len(extra_numbers)

        # Verify
        self._verify_seats(row)

        return created, updated, deleted

    def _strategy_create_only(self, row, current_seats):
        """Only create if no seats exist"""
        self.stdout.write(self.style.WARNING('\n   Executing CREATE-ONLY strategy...'))

        if current_seats.exists():
            self.stdout.write(self.style.NOTICE('   ℹ️  Seats already exist - skipping'))
            return 0, 0, 0

        # Update row
        row.numbering_style = 'vertical'
        row.position_y = 390
        row.save()
        self.stdout.write(self.style.SUCCESS('   ✅ Row updated'))

        # Create seats
        created = row.create_default_seats()
        self.stdout.write(self.style.SUCCESS(f'   ✅ Created {created} new seats'))

        # Verify
        self._verify_seats(row)

        return created, 0, 0

    def _verify_seats(self, row):
        """Verify all seats have correct position_y"""
        seats = row.seats.all().order_by('number')
        invalid = [s for s in seats if s.position_y == 0]

        self.stdout.write(f'\n   Verification:')
        self.stdout.write(f'      Total seats: {seats.count()}')

        if invalid:
            self.stdout.write(self.style.ERROR(f'      ❌ Invalid seats (position_y=0): {len(invalid)}'))
            for seat in invalid[:3]:
                self.stdout.write(self.style.ERROR(f'         Seat {seat.number}: position_y={seat.position_y}'))
        else:
            self.stdout.write(self.style.SUCCESS(f'      ✅ All seats valid'))
            # Show sample
            for seat in seats[:3]:
                self.stdout.write(self.style.SUCCESS(f'         ✅ Seat {seat.number}: position_y={seat.position_y}'))
            if seats.count() > 3:
                last_seat = seats.last()
                self.stdout.write(f'         ...')
                self.stdout.write(self.style.SUCCESS(
                    f'         ✅ Seat {last_seat.number}: position_y={last_seat.position_y}'))
