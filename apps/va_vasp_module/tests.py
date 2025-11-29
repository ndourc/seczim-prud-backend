from django.test import TestCase
from django.contrib.auth.models import User
from apps.core.models import SMI
from .models import VA_VASP, VirtualAsset, VASPService, VARiskAssessment, VASPCompliance

class VAVASPModuleTestCase(TestCase):
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
        
        # Create test VA/VASP analysis
        self.va_vasp = VA_VASP.objects.create(
            smi=self.smi,
            analysis_date='2023-01-01',
            is_va_issuer=True,
            is_vasp=True,
            va_types='Bitcoin, Ethereum',
            va_risk_score=65.0,
            vasp_risk_score=70.0,
            securities_exposure=25.50,
            regulatory_compliance=80.0
        )

    def test_va_vasp_creation(self):
        """Test creating a VA/VASP analysis"""
        va_vasp = VA_VASP.objects.create(
            smi=self.smi,
            analysis_date='2023-04-01',
            is_va_issuer=False,
            is_vasp=True,
            va_types='Bitcoin',
            va_risk_score=60.0,
            vasp_risk_score=75.0,
            securities_exposure=15.25,
            regulatory_compliance=85.0
        )
        self.assertEqual(va_vasp.smi, self.smi)
        self.assertFalse(va_vasp.is_va_issuer)
        self.assertTrue(va_vasp.is_vasp)

    def test_overall_va_risk_score_calculation(self):
        """Test overall VA risk score calculation"""
        # For both VA issuer and VASP, score should be weighted average
        expected_score = (65.0 * 0.4 + 70.0 * 0.6)
        self.va_vasp.calculate_overall_va_risk_score()
        self.assertEqual(self.va_vasp.overall_va_risk_score, round(expected_score, 2))

    def test_va_issuer_only_risk_score(self):
        """Test risk score calculation for VA issuer only"""
        va_vasp = VA_VASP.objects.create(
            smi=self.smi,
            analysis_date='2023-07-01',
            is_va_issuer=True,
            is_vasp=False,
            va_risk_score=80.0,
            vasp_risk_score=50.0
        )
        va_vasp.calculate_overall_va_risk_score()
        self.assertEqual(va_vasp.overall_va_risk_score, 80.0)

    def test_vasp_only_risk_score(self):
        """Test risk score calculation for VASP only"""
        va_vasp = VA_VASP.objects.create(
            smi=self.smi,
            analysis_date='2023-10-01',
            is_va_issuer=False,
            is_vasp=True,
            va_risk_score=50.0,
            vasp_risk_score=90.0
        )
        va_vasp.calculate_overall_va_risk_score()
        self.assertEqual(va_vasp.overall_va_risk_score, 90.0)

    def test_virtual_asset_creation(self):
        """Test creating a virtual asset"""
        asset = VirtualAsset.objects.create(
            va_vasp_analysis=self.va_vasp,
            asset_name='Bitcoin',
            asset_symbol='BTC',
            asset_category='CRYPTO',
            market_cap=500000000000,
            trading_volume=25000000000,
            volatility_index=75.5,
            risk_level='HIGH',
            risk_score=80.0,
            regulatory_status='Regulated'
        )
        self.assertEqual(asset.va_vasp_analysis, self.va_vasp)
        self.assertEqual(asset.asset_name, 'Bitcoin')
        self.assertEqual(asset.asset_symbol, 'BTC')
        self.assertEqual(asset.risk_level, 'HIGH')

    def test_vasp_service_creation(self):
        """Test creating a VASP service"""
        service = VASPService.objects.create(
            va_vasp_analysis=self.va_vasp,
            service_type='EXCHANGE',
            service_name='Crypto Exchange Service',
            service_description='Digital asset exchange platform',
            is_active=True,
            customer_count=10000,
            service_risk_score=70.0,
            compliance_status='Under Review'
        )
        self.assertEqual(service.va_vasp_analysis, self.va_vasp)
        self.assertEqual(service.service_type, 'EXCHANGE')
        self.assertEqual(service.service_name, 'Crypto Exchange Service')
        self.assertTrue(service.is_active)

    def test_va_risk_assessment_creation(self):
        """Test creating a VA risk assessment"""
        assessment = VARiskAssessment.objects.create(
            va_vasp_analysis=self.va_vasp,
            risk_category='MARKET_RISK',
            risk_score=75.0,
            risk_probability='HIGH',
            risk_impact='HIGH',
            risk_description='High market volatility risk',
            risk_factors='Market manipulation, regulatory changes',
            mitigation_strategies='Diversification, hedging strategies'
        )
        self.assertEqual(assessment.va_vasp_analysis, self.va_vasp)
        self.assertEqual(assessment.risk_category, 'MARKET_RISK')
        self.assertEqual(assessment.risk_probability, 'HIGH')
        self.assertEqual(assessment.risk_impact, 'HIGH')

    def test_vasp_compliance_creation(self):
        """Test creating VASP compliance record"""
        compliance = VASPCompliance.objects.create(
            va_vasp_analysis=self.va_vasp,
            compliance_area='KYC_AML',
            compliance_status='COMPLIANT',
            compliance_score=85.0,
            requirements='Customer identification, transaction monitoring',
            current_status='All requirements met',
            monitoring_frequency='DAILY'
        )
        self.assertEqual(compliance.va_vasp_analysis, self.va_vasp)
        self.assertEqual(compliance.compliance_area, 'KYC_AML')
        self.assertEqual(compliance.compliance_status, 'COMPLIANT')
        self.assertEqual(compliance.compliance_score, 85.0)

    def test_va_vasp_relationship_with_smi(self):
        """Test VA/VASP relationship with SMI"""
        self.assertEqual(self.va_vasp.smi, self.smi)
        self.assertEqual(self.smi.va_vasp_analyses.first(), self.va_vasp)

    def test_virtual_asset_relationship_with_va_vasp(self):
        """Test virtual asset relationship with VA/VASP analysis"""
        asset = VirtualAsset.objects.create(
            va_vasp_analysis=self.va_vasp,
            asset_name='Ethereum',
            asset_symbol='ETH',
            asset_category='CRYPTO'
        )
        self.assertEqual(asset.va_vasp_analysis, self.va_vasp)
        self.assertIn(asset, self.va_vasp.virtual_assets.all())
