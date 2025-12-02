from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from apps.auth_module.models import UserProfile
from apps.core.models import SMI
from django.db import transaction


class Command(BaseCommand):
    help = 'Create hardcoded users for SECZIM admin and SMI (Old Mutual)'

    def handle(self, *args, **kwargs):
        with transaction.atomic():
            # Create SECZIM Admin user
            admin_user, created = User.objects.get_or_create(
                username='admin',
                defaults={
                    'email': 'admin@seczim.gov.zw',
                    'first_name': 'SECZIM',
                    'last_name': 'Administrator',
                    'is_staff': True,
                    'is_superuser': True,
                }
            )
            if created or not admin_user.check_password('SecZim@2024!'):
                admin_user.set_password('SecZim@2024!')
                admin_user.save()
                self.stdout.write(self.style.SUCCESS(f'Created/Updated admin user: admin / SecZim@2024!'))
            
            # Create or update admin profile
            admin_profile, _ = UserProfile.objects.get_or_create(
                user=admin_user,
                defaults={
                    'role': 'ADMIN',
                    'department': 'Supervision',
                    'position': 'System Administrator',
                }
            )
            admin_profile.role = 'ADMIN'
            admin_profile.save()

            # Create or get Old Mutual SMI
            old_mutual_smi, created = SMI.objects.get_or_create(
                license_number='SMI-001-2024',
                defaults={
                    'company_name': 'Old Mutual Zimbabwe',
                    'business_type': 'Asset Management',
                    'address': 'Mutual Gardens, 100 The Chase West, Emerald Hill, Harare',
                    'phone': '+263 242 369 000',
                    'email': 'info@oldmutual.co.zw',
                    'website': 'https://www.oldmutual.co.zw',
                    'status': 'PENDING',  # Pending until they complete registration
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created SMI: {old_mutual_smi.company_name}'))

            # Create Old Mutual user
            smi_user, created = User.objects.get_or_create(
                username='oldmutual',
                defaults={
                    'email': 'compliance@oldmutual.co.zw',
                    'first_name': 'Old Mutual',
                    'last_name': 'Compliance',
                    'is_staff': False,
                    'is_superuser': False,
                }
            )
            if created or not smi_user.check_password('OldMutual@2024!'):
                smi_user.set_password('OldMutual@2024!')
                smi_user.save()
                self.stdout.write(self.style.SUCCESS(f'Created/Updated SMI user: oldmutual / OldMutual@2024!'))
            
            # Create or update SMI profile
            smi_profile, _ = UserProfile.objects.get_or_create(
                user=smi_user,
                defaults={
                    'role': 'SMI_USER',
                    'smi': old_mutual_smi,
                    'department': 'Compliance',
                    'position': 'Compliance Officer',
                }
            )
            smi_profile.role = 'SMI_USER'
            smi_profile.smi = old_mutual_smi
            smi_profile.save()

            self.stdout.write(self.style.SUCCESS('Successfully created hardcoded users!'))
            self.stdout.write(self.style.WARNING('Admin credentials: admin / SecZim@2024!'))
            self.stdout.write(self.style.WARNING('SMI credentials: oldmutual / OldMutual@2024!'))
