from django.test import TestCase
from django.contrib.auth.models import User
from apps.core.models import SMI
from .models import PrudentialReturn, IncomeStatement, BalanceSheet

class ReturnsModuleTestCase(TestCase):
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
        
        # Create test prudential return
        self.prudential_return = PrudentialReturn.objects.create(
            smi=self.smi,
            reporting_period='2023-01-01',
            submission_date='2023-02-15',
            status='SUBMITTED'
        )

    def test_prudential_return_creation(self):
        """Test creating a prudential return"""
        prudential_return = PrudentialReturn.objects.create(
            smi=self.smi,
            reporting_period='2023-04-01',
            submission_date='2023-05-15',
            status='DRAFT'
        )
        self.assertEqual(prudential_return.smi, self.smi)
        self.assertEqual(prudential_return.reporting_period, '2023-04-01')
        self.assertEqual(prudential_return.status, 'DRAFT')

    def test_income_statement_creation(self):
        """Test creating an income statement"""
        income_statement = IncomeStatement.objects.create(
            prudential_return=self.prudential_return,
            revenue=1000000.00,
            operating_expenses=750000.00,
            net_profit=250000.00
        )
        self.assertEqual(income_statement.prudential_return, self.prudential_return)
        self.assertEqual(income_statement.revenue, 1000000.00)
        self.assertEqual(income_statement.operating_expenses, 750000.00)
        self.assertEqual(income_statement.net_profit, 250000.00)

    def test_balance_sheet_creation(self):
        """Test creating a balance sheet"""
        balance_sheet = BalanceSheet.objects.create(
            prudential_return=self.prudential_return,
            total_assets=5000000.00,
            total_liabilities=3000000.00,
            equity=2000000.00
        )
        self.assertEqual(balance_sheet.prudential_return, self.prudential_return)
        self.assertEqual(balance_sheet.total_assets, 5000000.00)
        self.assertEqual(balance_sheet.total_liabilities, 3000000.00)
        self.assertEqual(balance_sheet.equity, 2000000.00)

    def test_prudential_return_status_choices(self):
        """Test prudential return status choices"""
        valid_statuses = ['DRAFT', 'SUBMITTED', 'UNDER_REVIEW', 'APPROVED', 'REJECTED']
        
        for status in valid_statuses:
            prudential_return = PrudentialReturn.objects.create(
                smi=self.smi,
                reporting_period=f'2023-{status.lower()}-01',
                submission_date='2023-02-15',
                status=status
            )
            self.assertEqual(prudential_return.status, status)

    def test_prudential_return_string_representation(self):
        """Test prudential return string representation"""
        expected_string = f"{self.smi.company_name} - {self.prudential_return.reporting_period}"
        self.assertEqual(str(self.prudential_return), expected_string)

    def test_income_statement_string_representation(self):
        """Test income statement string representation"""
        income_statement = IncomeStatement.objects.create(
            prudential_return=self.prudential_return,
            revenue=1000000.00,
            operating_expenses=750000.00,
            net_profit=250000.00
        )
        expected_string = f"{self.smi.company_name} - {self.prudential_return.reporting_period}"
        self.assertEqual(str(income_statement), expected_string)

    def test_balance_sheet_string_representation(self):
        """Test balance sheet string representation"""
        balance_sheet = BalanceSheet.objects.create(
            prudential_return=self.prudential_return,
            total_assets=5000000.00,
            total_liabilities=3000000.00,
            equity=2000000.00
        )
        expected_string = f"{self.smi.company_name} - {self.prudential_return.reporting_period}"
        self.assertEqual(str(balance_sheet), expected_string)

    def test_prudential_return_relationship_with_smi(self):
        """Test prudential return relationship with SMI"""
        self.assertEqual(self.prudential_return.smi, self.smi)
        self.assertIn(self.prudential_return, self.smi.prudentialreturn_set.all())

    def test_income_statement_relationship_with_prudential_return(self):
        """Test income statement relationship with prudential return"""
        income_statement = IncomeStatement.objects.create(
            prudential_return=self.prudential_return,
            revenue=1000000.00,
            operating_expenses=750000.00,
            net_profit=250000.00
        )
        self.assertEqual(income_statement.prudential_return, self.prudential_return)

    def test_balance_sheet_relationship_with_prudential_return(self):
        """Test balance sheet relationship with prudential return"""
        balance_sheet = BalanceSheet.objects.create(
            prudential_return=self.prudential_return,
            total_assets=5000000.00,
            total_liabilities=3000000.00,
            equity=2000000.00
        )
        self.assertEqual(balance_sheet.prudential_return, self.prudential_return)

    def test_prudential_return_ordering(self):
        """Test prudential return ordering by creation date"""
        # Create another return with later date
        later_return = PrudentialReturn.objects.create(
            smi=self.smi,
            reporting_period='2023-07-01',
            submission_date='2023-08-15',
            status='DRAFT'
        )
        
        # Test ordering (should be by creation date, newest first)
        returns = PrudentialReturn.objects.filter(smi=self.smi).order_by('-created_at')
        self.assertEqual(returns[0], later_return)
        self.assertEqual(returns[1], self.prudential_return)
