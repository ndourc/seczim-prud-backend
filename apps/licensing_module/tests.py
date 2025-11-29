from django.test import TestCase
from django.contrib.auth.models import User
from apps.core.models import SMI
from .models import LicensingPortalIntegration, PortalSMIData, InstitutionalProfile, Shareholder, Director, LicenseHistory

class LicensingModuleTestCase(TestCase):
    def setUp(self):
        # Create test user
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        # Create test SMI
        self.smi = SMI.objects.create(
            company_name='Test Company Ltd',
            license_number='TEST001',
            business_type='Financial Services'
        )
        
        # Create test portal integration
        self.portal_integration = LicensingPortalIntegration.objects.create(
            portal_name='Test Portal',
            api_endpoint='https://test-portal.com/api',
            status='ACTIVE'
        )

    def test_licensing_portal_integration_creation(self):
        """Test creating a licensing portal integration"""
        integration = LicensingPortalIntegration.objects.create(
            portal_name='Another Portal',
            api_endpoint='https://another-portal.com/api',
            status='INACTIVE'
        )
        self.assertEqual(integration.portal_name, 'Another Portal')
        self.assertEqual(integration.status, 'INACTIVE')
        self.assertEqual(integration.sync_frequency, 'DAILY')
        self.assertTrue(integration.auto_sync_enabled)

    def test_portal_smi_data_creation(self):
        """Test creating portal SMI data"""
        portal_data = PortalSMIData.objects.create(
            smi=self.smi,
            portal_id='PORTAL001',
            portal_status='Active',
            sync_status='SYNCED'
        )
        self.assertEqual(portal_data.smi, self.smi)
        self.assertEqual(portal_data.portal_id, 'PORTAL001')
        self.assertEqual(portal_data.portal_status, 'Active')
        self.assertEqual(portal_data.sync_status, 'SYNCED')

    def test_institutional_profile_creation(self):
        """Test creating institutional profile"""
        profile = InstitutionalProfile.objects.create(
            smi=self.smi,
            business_model='Traditional Banking',
            competitive_position='MID_TIER',
            financial_strength='GOOD',
            risk_appetite='MODERATE'
        )
        self.assertEqual(profile.smi, self.smi)
        self.assertEqual(profile.business_model, 'Traditional Banking')
        self.assertEqual(profile.competitive_position, 'MID_TIER')
        self.assertEqual(profile.financial_strength, 'GOOD')
        self.assertEqual(profile.risk_appetite, 'MODERATE')

    def test_shareholder_creation(self):
        """Test creating shareholder"""
        shareholder = Shareholder.objects.create(
            smi=self.smi,
            name='John Doe',
            shareholder_type='INDIVIDUAL',
            ownership_percentage=25.50
        )
        self.assertEqual(shareholder.smi, self.smi)
        self.assertEqual(shareholder.name, 'John Doe')
        self.assertEqual(shareholder.shareholder_type, 'INDIVIDUAL')
        self.assertEqual(shareholder.ownership_percentage, 25.50)
        self.assertTrue(shareholder.voting_rights)
        self.assertTrue(shareholder.is_active)

    def test_director_creation(self):
        """Test creating director"""
        director = Director.objects.create(
            smi=self.smi,
            name='Jane Smith',
            director_type='EXECUTIVE',
            appointment_date='2023-01-01'
        )
        self.assertEqual(director.smi, self.smi)
        self.assertEqual(director.name, 'Jane Smith')
        self.assertEqual(director.director_type, 'EXECUTIVE')
        self.assertEqual(director.appointment_date, '2023-01-01')
        self.assertTrue(director.is_active)

    def test_license_history_creation(self):
        """Test creating license history"""
        license_history = LicenseHistory.objects.create(
            smi=self.smi,
            change_type='GRANTED',
            change_date='2023-01-01',
            effective_date='2023-01-01',
            license_number='LIC001',
            license_type='Financial Services',
            license_scope='Full banking services',
            regulatory_authority='Central Bank'
        )
        self.assertEqual(license_history.smi, self.smi)
        self.assertEqual(license_history.change_type, 'GRANTED')
        self.assertEqual(license_history.license_number, 'LIC001')
        self.assertEqual(license_history.regulatory_authority, 'Central Bank')
        self.assertTrue(license_history.is_active)

    def test_licensing_portal_integration_string_representation(self):
        """Test licensing portal integration string representation"""
        expected_string = f"{self.portal_integration.portal_name} - {self.portal_integration.status}"
        self.assertEqual(str(self.portal_integration), expected_string)

    def test_portal_smi_data_string_representation(self):
        """Test portal SMI data string representation"""
        portal_data = PortalSMIData.objects.create(
            smi=self.smi,
            portal_id='PORTAL001',
            portal_status='Active'
        )
        expected_string = f"Portal Data - {self.smi.company_name}"
        self.assertEqual(str(portal_data), expected_string)

    def test_institutional_profile_string_representation(self):
        """Test institutional profile string representation"""
        profile = InstitutionalProfile.objects.create(
            smi=self.smi,
            business_model='Traditional Banking'
        )
        expected_string = f"Institutional Profile - {self.smi.company_name}"
        self.assertEqual(str(profile), expected_string)

    def test_shareholder_string_representation(self):
        """Test shareholder string representation"""
        shareholder = Shareholder.objects.create(
            smi=self.smi,
            name='John Doe',
            ownership_percentage=25.50
        )
        expected_string = f"John Doe - {self.smi.company_name} (25.50%)"
        self.assertEqual(str(shareholder), expected_string)

    def test_director_string_representation(self):
        """Test director string representation"""
        director = Director.objects.create(
            smi=self.smi,
            name='Jane Smith',
            director_type='EXECUTIVE',
            appointment_date='2023-01-01'
        )
        expected_string = f"Jane Smith - EXECUTIVE at {self.smi.company_name}"
        self.assertEqual(str(director), expected_string)

    def test_license_history_string_representation(self):
        """Test license history string representation"""
        license_history = LicenseHistory.objects.create(
            smi=self.smi,
            change_type='GRANTED',
            change_date='2023-01-01',
            effective_date='2023-01-01',
            license_number='LIC001',
            license_type='Financial Services',
            license_scope='Full banking services',
            regulatory_authority='Central Bank'
        )
        expected_string = f"GRANTED - {self.smi.company_name} - 2023-01-01"
        self.assertEqual(str(license_history), expected_string)

    def test_shareholder_ownership_percentage_validation(self):
        """Test shareholder ownership percentage validation"""
        # Test valid percentage
        shareholder = Shareholder.objects.create(
            smi=self.smi,
            name='Valid Shareholder',
            ownership_percentage=50.00
        )
        self.assertEqual(shareholder.ownership_percentage, 50.00)
        
        # Test boundary values
        shareholder2 = Shareholder.objects.create(
            smi=self.smi,
            name='Boundary Shareholder',
            ownership_percentage=100.00
        )
        self.assertEqual(shareholder2.ownership_percentage, 100.00)

    def test_director_fit_and_proper_assessment(self):
        """Test director fit and proper assessment"""
        director = Director.objects.create(
            smi=self.smi,
            name='Assessed Director',
            director_type='EXECUTIVE',
            appointment_date='2023-01-01',
            fit_and_proper_assessment='PASSED'
        )
        self.assertEqual(director.fit_and_proper_assessment, 'PASSED')

    def test_license_history_change_types(self):
        """Test license history change types"""
        valid_change_types = ['GRANTED', 'RENEWED', 'AMENDED', 'SUSPENDED', 'REVOKED', 'RESTORED', 'EXPIRED']
        
        for change_type in valid_change_types:
            license_history = LicenseHistory.objects.create(
                smi=self.smi,
                change_type=change_type,
                change_date='2023-01-01',
                effective_date='2023-01-01',
                license_number=f'LIC_{change_type}',
                license_type='Financial Services',
                license_scope='Test scope',
                regulatory_authority='Central Bank'
            )
            self.assertEqual(license_history.change_type, change_type)

    def test_institutional_profile_competitive_positions(self):
        """Test institutional profile competitive positions"""
        valid_positions = ['MARKET_LEADER', 'MAJOR_PLAYER', 'MID_TIER', 'SMALL_PLAYER', 'NICHE']
        
        for position in valid_positions:
            profile = InstitutionalProfile.objects.create(
                smi=self.smi,
                competitive_position=position
            )
            self.assertEqual(profile.competitive_position, position)

    def test_licensing_portal_integration_sync_frequencies(self):
        """Test licensing portal integration sync frequencies"""
        valid_frequencies = ['HOURLY', 'DAILY', 'WEEKLY', 'MANUAL']
        
        for frequency in valid_frequencies:
            integration = LicensingPortalIntegration.objects.create(
                portal_name=f'Portal {frequency}',
                api_endpoint=f'https://{frequency.lower()}-portal.com/api',
                sync_frequency=frequency
            )
            self.assertEqual(integration.sync_frequency, frequency)
