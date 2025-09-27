from django.core.management.base import BaseCommand
from venues.models import ContactInfo


class Command(BaseCommand):
    help = 'Setup default contact information'

    def handle(self, *args, **options):
        contact, created = ContactInfo.objects.get_or_create(
            pk=1,
            defaults={
                'name': 'Nhạc Kịch Giấc Mơ Chí Phèo',
                'hotline': '0962989856',
                'support_email': 'duongcamart@gmail.com',
                'facebook_url': 'https://www.facebook.com/nhackichgiacmochipheo',
                'tiktok_url': 'https://www.tiktok.com/@giacmo.chipheo',
                'logo_url': 'https://lh3.googleusercontent.com/pw/AP1GczOeY1ZKKsObbQ5Em5H14byD0GRz_-ydPBGZWzBOQbun4cB783CMb3NsYbucZAmrMlCE-YJ8r3Ll71Fthb-wyaMjuQbPTc1jAPLcf-3-NzjBqBuS_3NB2W6JzfAWZP3sRYBVzVxethfg4iJBam3EhoDp=w489-h301-s-no-gm',
                'copyright_text': 'GMCP by duongcamart'
            }
        )

        if created:
            self.stdout.write(self.style.SUCCESS('Created default contact information'))
        else:
            self.stdout.write(self.style.WARNING('Contact information already exists'))

        self.stdout.write(f'Contact: {contact.name}')
        self.stdout.write(f'Hotline: {contact.hotline_display}')
        self.stdout.write(f'Email: {contact.support_email}')


# backend/venues/fixtures/contact_info.json
[
    {
        "model": "venues.contactinfo",
        "pk": 1,
        "fields": {
            "name": "Nhạc Kịch Giấc Mơ Chí Phèo",
            "hotline": "0962989856",
            "support_email": "duongcamart@gmail.com",
            "facebook_url": "https://www.facebook.com/nhackichgiacmochipheo",
            "tiktok_url": "https://www.tiktok.com/@giacmo.chipheo",
            "instagram_url": "",
            "website_url": "",
            "logo_url": "https://lh3.googleusercontent.com/pw/AP1GczOeY1ZKKsObbQ5Em5H14byD0GRz_-ydPBGZWzBOQbun4cB783CMb3NsYbucZAmrMlCE-YJ8r3Ll71Fthb-wyaMjuQbPTc1jAPLcf-3-NzjBqBuS_3NB2W6JzfAWZP3sRYBVzVxethfg4iJBam3EhoDp=w489-h301-s-no-gm",
            "copyright_text": "GMCP by duongcamart"
        }
    }
]
