from django.test import TestCase
from django.contrib.auth.models import User
from apps.core.models import SMI
from .models import RiskAssessment, StressTest, RiskIndicator, RiskTrend

class RiskAssessmentModuleTestCase(TestCase):
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
        
        # Create test risk assessment
        self.risk_assessment = RiskAssessment.objects.create(
            smi=self.smi,
            assessment_date='2023-01-01',
            assessment_period='QUARTERLY',
            fsi_score=75.0,
            inherent_risk_score=60.0,
            operational_risk_score=70.0,
            market_risk_score=65.0,
            credit_risk_score=55.0,
            car=18.5,
            assessor=self.user
        )

    def test_risk_assessment_creation(self):
        """Test creating a risk assessment"""
        assessment = RiskAssessment.objects.create(
            smi=self.smi,
            assessment_date='2023-04-01',
            assessment_period='QUARTERLY',
            fsi_score=80.0,
            inherent_risk_score=65.0,
            operational_risk_score=75.0,
            market_risk_score=70.0,
            credit_risk_score=60.0,
            car=20.0,
            assessor=self.user
        )
        self.assertEqual(assessment.smi, self.smi)
        self.assertEqual(assessment.fsi_score, 80.0)

    def test_overall_risk_score_calculation(self):
        """Test overall risk score calculation"""
        # Calculate expected score based on weights
        expected_score = (75.0 * 0.25 + 60.0 * 0.20 + 70.0 * 0.20 + 65.0 * 0.15 + 55.0 * 0.20)
        self.risk_assessment.calculate_overall_risk_score()
        self.assertEqual(self.risk_assessment.overall_risk_score, round(expected_score, 2))

    def test_risk_level_determination(self):
        """Test risk level determination"""
        self.risk_assessment.calculate_overall_risk_score()
        self.risk_assessment.determine_risk_level()
        self.assertIn(self.risk_assessment.risk_level, ['LOW', 'MEDIUM_LOW', 'MEDIUM', 'MEDIUM_HIGH', 'HIGH', 'CRITICAL'])

    def test_stress_test_creation(self):
        """Test creating a stress test"""
        stress_test = StressTest.objects.create(
            smi=self.smi,
            test_date='2023-01-01',
            test_type='SMI_LEVEL',
            scenario_name='Economic Downturn',
            scenario_description='Simulation of economic downturn scenario',
            capital_adequacy_impact=-5.0,
            liquidity_impact=-3.0,
            passed=True
        )
        self.assertEqual(stress_test.smi, self.smi)
        self.assertEqual(stress_test.scenario_name, 'Economic Downturn')
        self.assertTrue(stress_test.passed)

    def test_risk_indicator_creation(self):
        """Test creating a risk indicator"""
        indicator = RiskIndicator.objects.create(
            smi=self.smi,
            indicator_date='2023-01-01',
            indicator_type='FINANCIAL',
            indicator_name='Capital Adequacy Ratio',
            current_value=18.5,
            threshold_value=15.0,
            trend='STABLE',
            is_breached=False,
            alert_level='LOW'
        )
        self.assertEqual(indicator.smi, self.smi)
        self.assertEqual(indicator.indicator_name, 'Capital Adequacy Ratio')
        self.assertFalse(indicator.is_breached)

    def test_risk_trend_creation(self):
        """Test creating a risk trend"""
        trend = RiskTrend.objects.create(
            smi=self.smi,
            period_start='2023-01-01',
            period_end='2023-03-31',
            risk_score_change=-5.0,
            risk_level_change='IMPROVED',
            financial_performance='POSITIVE',
            compliance_performance='POSITIVE',
            key_factors='Improved risk management practices',
            recommendations='Continue current risk management approach'
        )
        self.assertEqual(trend.smi, self.smi)
        self.assertEqual(trend.risk_level_change, 'IMPROVED')
        self.assertEqual(trend.financial_performance, 'POSITIVE')
