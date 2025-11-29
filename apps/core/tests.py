from django.test import TestCase
from django.contrib.auth.models import User
from .models import SMI, BoardMember, MeetingLog, ProductOffering, ClienteleProfile, FinancialStatement, ClientAssetMix, RiskAssessment, StressTest, InspectionReport, ComplianceIndex, LicensingBreach, SupervisoryIntervention, Case, VA_VASP, Notification, SystemAuditLog

class CoreModuleTestCase(TestCase):
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
            business_type='Financial Services',
            address='123 Test Street, Test City',
            phone='+1234567890',
            email='info@testcompany.com',
            website='https://testcompany.com'
        )

    def test_smi_creation(self):
        """Test creating an SMI"""
        smi = SMI.objects.create(
            company_name='Another Company Ltd',
            license_number='TEST002',
            business_type='Investment Services',
            address='456 Another Street, Another City',
            phone='+0987654321',
            email='info@anothercompany.com'
        )
        self.assertEqual(smi.company_name, 'Another Company Ltd')
        self.assertEqual(smi.license_number, 'TEST002')
        self.assertEqual(smi.business_type, 'Investment Services')

    def test_smi_string_representation(self):
        """Test SMI string representation"""
        expected_string = f"{self.smi.company_name} ({self.smi.license_number})"
        self.assertEqual(str(self.smi), expected_string)

    def test_smi_meta_ordering(self):
        """Test SMI meta ordering"""
        # Create another SMI
        smi2 = SMI.objects.create(
            company_name='Alpha Company Ltd',
            license_number='TEST003',
            business_type='Financial Services'
        )
        
        # Test ordering (should be alphabetical by company name)
        smis = SMI.objects.all().order_by('company_name')
        self.assertEqual(smis[0], smi2)  # Alpha comes before Test
        self.assertEqual(smis[1], self.smi)

    def test_board_member_creation(self):
        """Test creating a board member"""
        board_member = BoardMember.objects.create(
            smi=self.smi,
            name='John Doe',
            position='Chairman',
            appointment_date='2023-01-01'
        )
        self.assertEqual(board_member.smi, self.smi)
        self.assertEqual(board_member.name, 'John Doe')
        self.assertEqual(board_member.position, 'Chairman')
        self.assertTrue(board_member.is_active)

    def test_meeting_log_creation(self):
        """Test creating a meeting log"""
        meeting_log = MeetingLog.objects.create(
            smi=self.smi,
            meeting_date='2023-01-15',
            meeting_type='BOARD',
            attendees='John Doe, Jane Smith, Bob Johnson',
            agenda='Quarterly review and strategic planning',
            decisions='Approve new investment strategy',
            action_items='Implement new risk management framework'
        )
        self.assertEqual(meeting_log.smi, self.smi)
        self.assertEqual(meeting_log.meeting_type, 'BOARD')
        self.assertEqual(meeting_log.meeting_date, '2023-01-15')

    def test_product_offering_creation(self):
        """Test creating a product offering"""
        product = ProductOffering.objects.create(
            smi=self.smi,
            product_name='Investment Fund A',
            product_category='Mutual Fund',
            income_contribution=25.50
        )
        self.assertEqual(product.smi, self.smi)
        self.assertEqual(product.product_name, 'Investment Fund A')
        self.assertEqual(product.income_contribution, 25.50)

    def test_clientele_profile_creation(self):
        """Test creating a clientele profile"""
        profile = ClienteleProfile.objects.create(
            smi=self.smi,
            client_type='RETAIL',
            client_count=1000,
            income_contribution=30.00
        )
        self.assertEqual(profile.smi, self.smi)
        self.assertEqual(profile.client_type, 'RETAIL')
        self.assertEqual(profile.client_count, 1000)
        self.assertEqual(profile.income_contribution, 30.00)

    def test_financial_statement_creation(self):
        """Test creating a financial statement"""
        statement = FinancialStatement.objects.create(
            smi=self.smi,
            period='2023-01-01',
            statement_type='FINANCIAL_POSITION',
            total_assets=10000000.00,
            total_liabilities=6000000.00,
            total_equity=4000000.00,
            total_revenue=2000000.00,
            total_expenses=1500000.00,
            net_profit=500000.00
        )
        self.assertEqual(statement.smi, self.smi)
        self.assertEqual(statement.statement_type, 'FINANCIAL_POSITION')
        self.assertEqual(statement.total_assets, 10000000.00)

    def test_client_asset_mix_creation(self):
        """Test creating a client asset mix"""
        asset_mix = ClientAssetMix.objects.create(
            smi=self.smi,
            period='2023-01-01',
            asset_class='EQUITIES',
            allocation_percentage=40.00,
            market_value=4000000.00,
            net_capital_position=3500000.00
        )
        self.assertEqual(asset_mix.smi, self.smi)
        self.assertEqual(asset_mix.asset_class, 'EQUITIES')
        self.assertEqual(asset_mix.allocation_percentage, 40.00)

    def test_risk_assessment_creation(self):
        """Test creating a risk assessment"""
        assessment = RiskAssessment.objects.create(
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
        self.assertEqual(assessment.smi, self.smi)
        self.assertEqual(assessment.fsi_score, 75.0)
        self.assertEqual(assessment.assessor, self.user)

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

    def test_inspection_report_creation(self):
        """Test creating an inspection report"""
        report = InspectionReport.objects.create(
            smi=self.smi,
            inspection_type='ONSITE',
            inspection_date='2023-01-15',
            inspector=self.user,
            executive_summary='Overall compliance is satisfactory',
            scope='Comprehensive onsite inspection',
            methodology='Risk-based inspection approach',
            findings='Minor gaps in documentation',
            severity='MEDIUM',
            risk_areas='CDD, record-keeping'
        )
        self.assertEqual(report.smi, self.smi)
        self.assertEqual(report.inspection_type, 'ONSITE')
        self.assertEqual(report.inspector, self.user)

    def test_compliance_index_creation(self):
        """Test creating a compliance index"""
        index = ComplianceIndex.objects.create(
            smi=self.smi,
            period='2023-01-01',
            analysis_period='QUARTERLY',
            overall_compliance_score=80.0,
            regulatory_compliance=85.0,
            operational_compliance=75.0,
            financial_compliance=80.0,
            risk_calibration_score=78.0
        )
        self.assertEqual(index.smi, self.smi)
        self.assertEqual(index.overall_compliance_score, 80.0)
        self.assertEqual(index.analysis_period, 'QUARTERLY')

    def test_licensing_breach_creation(self):
        """Test creating a licensing breach"""
        breach = LicensingBreach.objects.create(
            smi=self.smi,
            breach_type='MINOR',
            breach_date='2023-02-01',
            description='Late submission of quarterly report',
            regulatory_reference='Section 25 of Financial Services Act',
            status='OPEN',
            assigned_to=self.user
        )
        self.assertEqual(breach.smi, self.smi)
        self.assertEqual(breach.breach_type, 'MINOR')
        self.assertEqual(breach.assigned_to, self.user)

    def test_supervisory_intervention_creation(self):
        """Test creating a supervisory intervention"""
        intervention = SupervisoryIntervention.objects.create(
            smi=self.smi,
            intervention_type='WARNING',
            intervention_date='2023-02-15',
            reason='Late submission of required reports',
            description='Written warning issued for late submissions',
            intensity='MEDIUM',
            frequency='ONE_TIME'
        )
        self.assertEqual(intervention.smi, self.smi)
        self.assertEqual(intervention.intervention_type, 'WARNING')
        self.assertEqual(intervention.intensity, 'MEDIUM')

    def test_case_creation(self):
        """Test creating a case"""
        case = Case.objects.create(
            case_type='INVESTIGATION',
            title='Test Investigation Case',
            description='Test case description',
            smi=self.smi,
            assigned_to=self.user,
            status='OPEN',
            priority='MEDIUM'
        )
        self.assertEqual(case.smi, self.smi)
        self.assertEqual(case.case_type, 'INVESTIGATION')
        self.assertEqual(case.assigned_to, self.user)
        self.assertIsNotNone(case.case_number)

    def test_va_vasp_creation(self):
        """Test creating a VA/VASP analysis"""
        va_vasp = VA_VASP.objects.create(
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
        self.assertEqual(va_vasp.smi, self.smi)
        self.assertTrue(va_vasp.is_va_issuer)
        self.assertTrue(va_vasp.is_vasp)

    def test_notification_creation(self):
        """Test creating a notification"""
        notification = Notification.objects.create(
            user=self.user,
            notification_type='RISK_THRESHOLD',
            title='Risk Threshold Alert',
            message='Risk score has exceeded threshold',
            priority='HIGH',
            content_link='https://example.com/risk-details'
        )
        self.assertEqual(notification.user, self.user)
        self.assertEqual(notification.notification_type, 'RISK_THRESHOLD')
        self.assertEqual(notification.priority, 'HIGH')

    def test_system_audit_log_creation(self):
        """Test creating a system audit log"""
        audit_log = SystemAuditLog.objects.create(
            user=self.user,
            action='CREATE',
            model_name='SMI',
            object_id=str(self.smi.id),
            object_repr=str(self.smi),
            change_message='SMI created successfully'
        )
        self.assertEqual(audit_log.user, self.user)
        self.assertEqual(audit_log.action, 'CREATE')
        self.assertEqual(audit_log.model_name, 'SMI')
