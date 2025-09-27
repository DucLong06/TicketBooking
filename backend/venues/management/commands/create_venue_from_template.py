
from django.core.management.base import BaseCommand, CommandError
from venues.models import Venue, VenueLayout, Section, Row, Seat, PriceCategory, VENUE_TYPES
from venues.venue_templates import VENUE_TEMPLATES
import json


class Command(BaseCommand):
    help = 'Tạo venue từ template'

    def add_arguments(self, parser):
        parser.add_argument(
            '--template',
            type=str,
            required=True,
            choices=VENUE_TEMPLATES.keys(),
            help='Template name (ho_guom_opera, standard_theater)'
        )
        parser.add_argument(
            '--name',
            type=str,
            required=True,
            help='Tên nhà hát'
        )
        parser.add_argument(
            '--address',
            type=str,
            required=True,
            help='Địa chỉ nhà hát'
        )
        parser.add_argument(
            '--phone',
            type=str,
            default='',
            help='Số điện thoại'
        )
        parser.add_argument(
            '--email',
            type=str,
            default='',
            help='Email'
        )
        parser.add_argument(
            '--force',
            action='store_true',
            help='Ghi đè venue nếu đã tồn tại'
        )

    def handle(self, *args, **options):
        template_name = options['template']
        template = VENUE_TEMPLATES[template_name]

        self.stdout.write(
            self.style.SUCCESS(f'Tạo venue từ template: {template["name"]}')
        )

        # 1. Tạo hoặc lấy VenueLayout
        layout, created = VenueLayout.objects.get_or_create(
            name=template['name'],
            venue_type=template['type'],
            defaults={
                'description': template.get('description', ''),
                'config': template,
                'is_template': True
            }
        )

        if created:
            self.stdout.write(f'Tạo layout template: {layout.name}')
        else:
            self.stdout.write(f'Sử dụng layout có sẵn: {layout.name}')

        # 2. Kiểm tra venue đã tồn tại
        if Venue.objects.filter(name=options['name']).exists():
            if not options['force']:
                raise CommandError(f'Venue "{options["name"]}" đã tồn tại. Dùng --force để ghi đè.')
            else:
                # Xóa venue cũ
                old_venue = Venue.objects.get(name=options['name'])
                old_venue.delete()
                self.stdout.write(f'Đã xóa venue cũ: {options["name"]}')

        # 3. Tạo venue mới
        venue = Venue.objects.create(
            name=options['name'],
            address=options['address'],
            phone=options.get('phone', ''),
            email=options.get('email', ''),
            layout=layout,
            venue_type=template['type']
        )

        self.stdout.write(f'Tạo venue: {venue.name}')

        # 4. Tạo price categories
        self.create_price_categories(template.get('price_categories', {}))

        # 5. Tạo layout từ config
        self.create_venue_layout(venue, template)

        self.stdout.write(
            self.style.SUCCESS(f'Hoàn thành! Venue "{venue.name}" đã được tạo với {venue.total_seats} ghế.')
        )

    def create_price_categories(self, categories_config):
        """Tạo price categories từ config"""
        for code, config in categories_config.items():
            category, created = PriceCategory.objects.get_or_create(
                code=code,
                defaults={
                    'name': config['name'],
                    'base_price': config['base_price'],
                    'color': config['color']
                }
            )
            if created:
                self.stdout.write(f'Tạo price category: {category.name}')

    def create_venue_layout(self, venue, template):
        """Tạo sections, rows, seats từ template"""
        for floor in template.get('floors', []):
            for section_config in floor.get('sections', []):
                # Tạo section
                section = Section.objects.create(
                    venue=venue,
                    name=section_config['name'],
                    code=section_config['id'],
                    position_x=section_config.get('position', {}).get('x', 0),
                    position_y=section_config.get('position', {}).get('y', 0),
                    order=len(venue.sections.all()) + 1
                )

                self.stdout.write(f'Tạo section: {section.name}')

                # Tạo rows cho section
                for row_config in section_config.get('rows', []):
                    self.create_row_with_seats(section, row_config)

    def create_row_with_seats(self, section, row_config):
        """Tạo row và seats với numbering system mới"""
        # Lấy price category
        category_code = row_config.get('category', 'standard')
        try:
            price_category = PriceCategory.objects.get(code=category_code)
        except PriceCategory.DoesNotExist:
            price_category = PriceCategory.objects.first()
            self.stdout.write(
                self.style.WARNING(f'Không tìm thấy category {category_code}, dùng {price_category.code}')
            )

        # Tạo row với numbering config
        row = Row.objects.create(
            section=section,
            label=row_config['label'],
            seat_count=row_config['seats'],
            position_y=row_config.get('position_y', 0),
            price_category=price_category,
            numbering_style=row_config.get('numbering', 'center_out'),
            center_x=row_config.get('center_x', 400),
            aisle_width=row_config.get('aisle_width', 60),
            has_center_aisle=row_config.get('center_x', 400) > 0,
            gaps=row_config.get('gaps', [])
        )

        # Tạo seats theo numbering system của row
        self.create_seats_for_row(row)

        self.stdout.write(f'Tạo row {row.label} với {row_config["seats"]} ghế ({row.numbering_style})')

    def create_seats_for_row(self, row):
        """Tạo ghế cho row theo numbering system"""
        seat_positions = row.actual_seat_positions

        for seat_num, pos in seat_positions.items():
            Seat.objects.create(
                row=row,
                number=seat_num,
                position_x=pos['x'],
                position_y=pos['y'],
                status='active'
            )
