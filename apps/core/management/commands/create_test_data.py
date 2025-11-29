from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from apps.core.models import SMI

class Command(BaseCommand):
    help = 'Creates test data for development'

    def handle(self, *args, **kwargs):
        # Create test user if doesn't exist
        if not User.objects.filter(username='testuser').exists():
            User.objects.create_user(
                username='testuser',
                password='testpass123',
                email='test@example.com'
            )
            self.stdout.write(self.style.SUCCESS('Created test user'))

        # Create test SMIs
        test_smis = [
            {
                'company_name': 'Alpha Securities Ltd',
                'license_number': 'SEC001'
            },
            {
                'company_name': 'Beta Investments Inc',
                'license_number': 'SEC002'
            },
            {
                'company_name': 'Gamma Trading Co',
                'license_number': 'SEC003'
            }
        ]

        for smi_data in test_smis:
            SMI.objects.get_or_create(**smi_data)

        self.stdout.write(self.style.SUCCESS('Created test SMIs'))
