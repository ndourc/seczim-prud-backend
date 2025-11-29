from django.test import TestCase
from django.contrib.auth.models import User
from apps.core.models import SMI
from .models import ComplianceIndex, ComplianceAssessment, ComplianceRequirement, ComplianceViolation, ComplianceReport

class ComplianceModuleTestCase(TestCase):
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
        
        # Create test compliance index
        self.compliance_index = ComplianceIndex.objects.create(
            smi=self.smi,
            period='2023-01-01',
            analysis_period='QUARTERLY',
            overall_compliance_score=80.0,
            regulatory_compliance=85.0,
            operational_compliance=75.0,
            financial_compliance=80.0,
            risk_calibration_score=78.0,
            risk_adjustment_factor=1.0,
            post_inspection_adjustment=2.0
        )

    def test_compliance_index_creation(self):
        """Test creating a compliance index"""
        index = ComplianceIndex.objects.create(
            smi=self.smi,
            period='2023-04-01',
            analysis_period='QUARTERLY',
            overall_compliance_score=85.0,
            regulatory_compliance=90.0,
            operational_compliance=80.0,
            financial_compliance=85.0,
            risk_calibration_score=82.0
        )
        self.assertEqual(index.smi, self.smi)
        self.assertEqual(index.overall_compliance_score, 85.0)
        self.assertEqual(index.analysis_period, 'QUARTERLY')

    def test_final_compliance_score_calculation(self):
        """Test final compliance score calculation"""
        # Calculate expected final score
        expected_score = self.compliance_index.overall_compliance_score + self.compliance_index.post_inspection_adjustment
        self.compliance_index.calculate_final_compliance_score()
        self.assertEqual(self.compliance_index.final_compliance_score, expected_score)

    def test_compliance_assessment_creation(self):
        """Test creating a compliance assessment"""
        assessment = ComplianceAssessment.objects.create(
            smi=self.smi,
            assessment_date='2023-01-01',
            assessment_type='REGULAR',
            scope='Comprehensive compliance assessment',
            methodology='Risk-based assessment approach',
            risk_areas={'CDD': 'Customer Due Diligence', 'record_keeping': 'Documentation'},
            findings='Overall compliance is satisfactory with minor gaps',
            compliance_gaps='Some documentation improvements needed',
            risk_rating='MEDIUM',
            recommendations='Enhance record-keeping procedures',
            status='COMPLETED'
        )
        self.assertEqual(assessment.smi, self.smi)
        self.assertEqual(assessment.assessment_type, 'REGULAR')
        self.assertEqual(assessment.risk_rating, 'MEDIUM')
        self.assertEqual(assessment.status, 'COMPLETED')

    def test_compliance_requirement_creation(self):
        """Test creating a compliance requirement"""
        requirement = ComplianceRequirement.objects.create(
            smi=self.smi,
            requirement_type='REGULATORY',
            title='Capital Adequacy Requirements',
            description='Maintain minimum capital adequacy ratio of 15%',
            regulatory_reference='Section 45 of Financial Services Act',
            priority='HIGH',
            is_compliant=True,
            compliance_score=95.0,
            effective_date='2023-01-01',
            monitoring_frequency='MONTHLY'
        )
        self.assertEqual(requirement.smi, self.smi)
        self.assertEqual(requirement.requirement_type, 'REGULATORY')
        self.assertEqual(requirement.priority, 'HIGH')
        self.assertTrue(requirement.is_compliant)

    def test_compliance_violation_creation(self):
        """Test creating a compliance violation"""
        requirement = ComplianceRequirement.objects.create(
            smi=self.smi,
            requirement_type='REPORTING',
            title='Quarterly Reporting',
            description='Submit quarterly financial reports',
            priority='MEDIUM'
        )
        
        violation = ComplianceViolation.objects.create(
            smi=self.smi,
            compliance_requirement=requirement,
            violation_type='MINOR',
            severity='LOW',
            description='Late submission of quarterly report',
            date_identified='2023-02-01',
            investigation_status='RESOLVED',
            corrective_actions='Implemented automated reminder system',
            preventive_measures='Enhanced reporting procedures'
        )
        self.assertEqual(violation.smi, self.smi)
        self.assertEqual(violation.violation_type, 'MINOR')
        self.assertEqual(violation.severity, 'LOW')
        self.assertEqual(violation.investigation_status, 'RESOLVED')

    def test_compliance_report_creation(self):
        """Test creating a compliance report"""
        report = ComplianceReport.objects.create(
            smi=self.smi,
            report_type='QUARTERLY',
            title='Q1 2023 Compliance Report',
            period_start='2023-01-01',
            period_end='2023-03-31',
            report_date='2023-04-15',
            executive_summary='Overall compliance status is satisfactory',
            findings='Minor gaps identified in documentation',
            recommendations='Enhance record-keeping procedures',
            action_items=['Implement new documentation system', 'Train staff on new procedures'],
            status='APPROVED',
            prepared_by=self.user
        )
        self.assertEqual(report.smi, self.smi)
        self.assertEqual(report.report_type, 'QUARTERLY')
        self.assertEqual(report.title, 'Q1 2023 Compliance Report')
        self.assertEqual(report.status, 'APPROVED')

    def test_compliance_index_unique_constraint(self):
        """Test unique constraint on compliance index"""
        # Try to create another compliance index with same SMI, period, and analysis_period
        with self.assertRaises(Exception):
            ComplianceIndex.objects.create(
                smi=self.smi,
                period='2023-01-01',
                analysis_period='QUARTERLY',
                overall_compliance_score=90.0
            )

    def test_compliance_requirement_priority_ordering(self):
        """Test compliance requirement ordering by priority and due date"""
        # Create requirements with different priorities and due dates
        req1 = ComplianceRequirement.objects.create(
            smi=self.smi,
            requirement_type='REGULATORY',
            title='High Priority Requirement',
            description='Critical regulatory requirement',
            priority='HIGH',
            due_date='2023-12-31'
        )
        
        req2 = ComplianceRequirement.objects.create(
            smi=self.smi,
            requirement_type='OPERATIONAL',
            title='Medium Priority Requirement',
            description='Standard operational requirement',
            priority='MEDIUM',
            due_date='2023-06-30'
        )
        
        # Test ordering
        requirements = ComplianceRequirement.objects.filter(smi=self.smi).order_by('due_date', 'priority')
        self.assertEqual(requirements[0], req2)  # Earlier due date
        self.assertEqual(requirements[1], req1)  # Later due date
