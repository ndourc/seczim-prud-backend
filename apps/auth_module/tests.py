from django.test import TestCase
from django.contrib.auth.models import User
from apps.core.models import SMI
from .models import UserProfile

class AuthModuleTestCase(TestCase):
    def setUp(self):
        # Create test user
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )
        
        # Create test SMI
        self.smi = SMI.objects.create(
            company_name='Test Company Ltd',
            license_number='TEST001',
            business_type='Financial Services'
        )
        
        # Create test user profile
        self.user_profile = UserProfile.objects.create(
            user=self.user,
            smi=self.smi,
            role='COMPLIANCE_OFFICER',
            phone_number='+1234567890'
        )

    def test_user_profile_creation(self):
        """Test creating a user profile"""
        new_user = User.objects.create_user(
            username='newuser',
            password='newpass123',
            email='new@example.com'
        )
        
        profile = UserProfile.objects.create(
            user=new_user,
            smi=self.smi,
            role='ACCOUNTANT',
            phone_number='+0987654321'
        )
        
        self.assertEqual(profile.user, new_user)
        self.assertEqual(profile.smi, self.smi)
        self.assertEqual(profile.role, 'ACCOUNTANT')
        self.assertEqual(profile.phone_number, '+0987654321')

    def test_user_profile_role_choices(self):
        """Test user profile role choices"""
        valid_roles = ['ADMIN', 'PRINCIPAL_OFFICER', 'ACCOUNTANT', 'COMPLIANCE_OFFICER']
        
        for role in valid_roles:
            user = User.objects.create_user(
                username=f'user_{role.lower()}',
                password='pass123',
                email=f'{role.lower()}@example.com'
            )
            
            profile = UserProfile.objects.create(
                user=user,
                smi=self.smi,
                role=role
            )
            self.assertEqual(profile.role, role)

    def test_user_profile_string_representation(self):
        """Test user profile string representation"""
        expected_string = f"{self.user.username} - {self.user_profile.role}"
        self.assertEqual(str(self.user_profile), expected_string)

    def test_user_profile_relationship_with_user(self):
        """Test user profile relationship with user"""
        self.assertEqual(self.user_profile.user, self.user)
        self.assertEqual(self.user.userprofile, self.user_profile)

    def test_user_profile_relationship_with_smi(self):
        """Test user profile relationship with SMI"""
        self.assertEqual(self.user_profile.smi, self.smi)
        self.assertIn(self.user_profile, self.smi.userprofile_set.all())

    def test_user_profile_permissions(self):
        """Test user profile permissions"""
        # Test that permissions are properly set
        permissions = self.user_profile._meta.permissions
        expected_permissions = [
            ("can_view_smi_data", "Can view SMI data"),
            ("can_edit_smi_data", "Can edit SMI data"),
            ("can_view_reports", "Can view reports"),
            ("can_create_reports", "Can create reports"),
        ]
        
        for permission in expected_permissions:
            self.assertIn(permission, permissions)

    def test_user_profile_without_smi(self):
        """Test user profile without SMI (for admin users)"""
        admin_user = User.objects.create_user(
            username='adminuser',
            password='adminpass123',
            email='admin@example.com'
        )
        
        profile = UserProfile.objects.create(
            user=admin_user,
            role='ADMIN'
        )
        
        self.assertEqual(profile.user, admin_user)
        self.assertEqual(profile.role, 'ADMIN')
        self.assertIsNone(profile.smi)

    def test_user_profile_phone_number_optional(self):
        """Test that phone number is optional"""
        user = User.objects.create_user(
            username='phoneuser',
            password='phonepass123',
            email='phone@example.com'
        )
        
        profile = UserProfile.objects.create(
            user=user,
            smi=self.smi,
            role='PRINCIPAL_OFFICER'
        )
        
        self.assertEqual(profile.user, user)
        self.assertEqual(profile.role, 'PRINCIPAL_OFFICER')
        self.assertEqual(profile.phone_number, '')

    def test_user_profile_meta_ordering(self):
        """Test user profile meta ordering"""
        # Create multiple profiles
        user1 = User.objects.create_user(username='user1', password='pass1')
        user2 = User.objects.create_user(username='user2', password='pass2')
        
        profile1 = UserProfile.objects.create(user=user1, smi=self.smi, role='ACCOUNTANT')
        profile2 = UserProfile.objects.create(user=user2, smi=self.smi, role='COMPLIANCE_OFFICER')
        
        # Test ordering (should be by creation date, newest first)
        profiles = UserProfile.objects.filter(smi=self.smi).order_by('-created_at')
        self.assertEqual(profiles[0], profile2)
        self.assertEqual(profiles[1], profile1)
        self.assertEqual(profiles[2], self.user_profile)
