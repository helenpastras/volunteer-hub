from django.core.management.base import BaseCommand
from my_app.models import Tag

class Command(BaseCommand):
    help = 'Seed default tags into the database'

    def handle(self, *args, **kwargs):
        tags = [
            'Environment', 'Education', 'Arts & Culture', 'Health',
            'Community Support', 'Tech & Innovation', 'Youth Programs',
            'Animal Welfare', 'Food Security', 'Disaster Relief'
        ]
        for name in tags:
            Tag.objects.get_or_create(name=name)
        self.stdout.write(self.style.SUCCESS('Tags seeded successfully!'))