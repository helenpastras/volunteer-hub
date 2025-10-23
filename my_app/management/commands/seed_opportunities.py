from django.core.management.base import BaseCommand
from my_app.models import Opportunity, Tag, User

class Command(BaseCommand):
    help = 'Seed sample opportunities for demo users'

    def handle(self, *args, **kwargs):
        users = {
        
            'melly': [
                {
                    'title': 'Beach Cleanup Crew',
                    'location': 'Long Island, NY',
                    'description': 'Join us to restore the shoreline!',
                    'tags': ['Environment', 'Community Support'],
                    'date': '2025-11-01'
                }, 
                {
                    'title': 'Youth Coding Mentor',
                    'location': 'Remote',
                    'description': 'Help teens learn Python basics.',
                    'tags': ['Tech & Innovation', 'Youth Programs'],
                    'date': '2025-11-10'
                }
            ],
            'alex': [
                {
                    'title': 'Community Mural Painting',
                    'location': 'Brooklyn, NY',
                    'description': 'Help bring color and joy to a local school wall.',
                    'tags': ['Arts & Culture', 'Youth Programs'],
                    'date': '2025-11-05'
                }
            ],
            'sam': [
                {
                    'title': 'Disaster Relief Packing',
                    'location': 'Queens, NY',
                    'description': 'Assemble emergency kits for families affected by recent floods.',
                    'tags': ['Disaster Relief', 'Community Support'],
                    'date': '2025-11-08'
                }
            ]
        }
                

    

        for username, opps in users.items():
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                self.stdout.write(self.style.WARNING(f'User {username} not found'))
                continue

            for opp in opps:
                opportunity = Opportunity.objects.create(
                    title=opp['title'],
                    location=opp['location'],
                    description=opp['description'],
                    date=opp['date'],
                    created_by=user
                )
                for tag_name in opp['tags']:
                    tag = Tag.objects.get(name=tag_name)
                    opportunity.tags.add(tag)

        self.stdout.write(self.style.SUCCESS('Opportunities seeded successfully!'))