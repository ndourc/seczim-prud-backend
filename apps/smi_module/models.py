from django.db import models
from django.utils import timezone
from apps.core.models import SMI


class ReportingPeriod(models.Model):
    start = models.DateField()
    end = models.DateField()

    def __str__(self):
        return f"{self.start} to {self.end}"


class SMISubmission(models.Model):
    smi = models.ForeignKey(SMI, on_delete=models.CASCADE, related_name='smi_submissions')
    reporting_period = models.OneToOneField(ReportingPeriod, on_delete=models.CASCADE, related_name='submission')

    # Metadata and audit
    submitted_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Submission for {self.smi.company_name} ({self.reporting_period})"


class BoardMember(models.Model):
    submission = models.ForeignKey(SMISubmission, on_delete=models.CASCADE, related_name='board_members')
    name = models.CharField(max_length=255)
    position = models.CharField(max_length=255)
    appointment_date = models.DateField()
    qualifications = models.TextField(blank=True)
    experience = models.TextField(blank=True)
    is_pep = models.BooleanField(default=False)
    frontend_id = models.CharField(max_length=64, blank=True)  # optional storage of frontend id


class Committee(models.Model):
    submission = models.ForeignKey(SMISubmission, on_delete=models.CASCADE, related_name='committees')
    name = models.CharField(max_length=255)
    purpose = models.TextField(blank=True)
    chairperson = models.CharField(max_length=255, blank=True)
    members = models.JSONField(default=list)  # list of names
    meetings_held = models.IntegerField(default=0)
    meeting_frequency = models.CharField(max_length=100, blank=True)
    frontend_id = models.CharField(max_length=64, blank=True)


class Product(models.Model):
    submission = models.ForeignKey(SMISubmission, on_delete=models.CASCADE, related_name='products')
    product_name = models.CharField(max_length=255)
    product_type = models.CharField(max_length=255)
    launch_date = models.DateField(null=True, blank=True)
    income = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    concentration_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    frontend_id = models.CharField(max_length=64, blank=True)


class Client(models.Model):
    submission = models.ForeignKey(SMISubmission, on_delete=models.CASCADE, related_name='clients')
    client_name = models.CharField(max_length=255)
    client_type = models.CharField(max_length=255)
    onboarding_date = models.DateField(null=True, blank=True)
    income = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    concentration_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    frontend_id = models.CharField(max_length=64, blank=True)


class FinancialStatement(models.Model):
    submission = models.OneToOneField(SMISubmission, on_delete=models.CASCADE, related_name='financial_statement')
    period_start = models.DateField()
    period_end = models.DateField()
    total_revenue = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    operating_costs = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    profit_before_tax = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    gross_margin = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    profit_margin = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)


class IncomeItem(models.Model):
    financial_statement = models.ForeignKey(FinancialStatement, on_delete=models.CASCADE, related_name='income_items')
    category = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    amount = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    is_core = models.BooleanField(default=False)
    frontend_id = models.CharField(max_length=64, blank=True)


class BalanceSheet(models.Model):
    submission = models.OneToOneField(SMISubmission, on_delete=models.CASCADE, related_name='balance_sheet')
    period_end = models.DateField()
    shareholders_funds = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    total_assets = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    total_liabilities = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    current_assets = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    current_liabilities = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    working_capital = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    cash_cover = models.DecimalField(max_digits=18, decimal_places=2, default=0)


class BalanceAsset(models.Model):
    balance_sheet = models.ForeignKey(BalanceSheet, on_delete=models.CASCADE, related_name='assets')
    asset_type = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    value = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    is_current = models.BooleanField(default=False)
    acquisition_date = models.DateField(null=True, blank=True)
    frontend_id = models.CharField(max_length=64, blank=True)


class BalanceLiability(models.Model):
    balance_sheet = models.ForeignKey(BalanceSheet, on_delete=models.CASCADE, related_name='liabilities')
    liability_type = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    value = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    is_current = models.BooleanField(default=False)
    due_date = models.DateField(null=True, blank=True)
    frontend_id = models.CharField(max_length=64, blank=True)


class Debtor(models.Model):
    balance_sheet = models.ForeignKey(BalanceSheet, on_delete=models.CASCADE, related_name='debtors')
    name = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    age_days = models.IntegerField(default=0)
    frontend_id = models.CharField(max_length=64, blank=True)


class Creditor(models.Model):
    balance_sheet = models.ForeignKey(BalanceSheet, on_delete=models.CASCADE, related_name='creditors')
    name = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    due_date = models.DateField(null=True, blank=True)
    frontend_id = models.CharField(max_length=64, blank=True)


class RelatedParty(models.Model):
    balance_sheet = models.ForeignKey(BalanceSheet, on_delete=models.CASCADE, related_name='related_parties')
    name = models.CharField(max_length=255)
    relationship = models.CharField(max_length=255)
    balance = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    type = models.CharField(max_length=64)
    frontend_id = models.CharField(max_length=64, blank=True)


class ClientAsset(models.Model):
    submission = models.ForeignKey(SMISubmission, on_delete=models.CASCADE, related_name='client_assets')
    asset_type = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    value = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    is_current = models.BooleanField(default=False)
    acquisition_date = models.DateField(null=True, blank=True)
    concentration_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    frontend_id = models.CharField(max_length=64, blank=True)


class CapitalPosition(models.Model):
    submission = models.OneToOneField(SMISubmission, on_delete=models.CASCADE, related_name='capital_position')
    calculation_date = models.DateField()
    net_capital = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    required_capital = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    adjusted_liquid_capital = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    is_compliant = models.BooleanField(default=False)
    capital_adequacy_ratio = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)


class SubmissionMetadata(models.Model):
    submission = models.OneToOneField(SMISubmission, on_delete=models.CASCADE, related_name='metadata')
    submitted_at = models.DateTimeField(null=True, blank=True)
    total_board_members = models.IntegerField(default=0)
    total_committees = models.IntegerField(default=0)
    total_products = models.IntegerField(default=0)
    total_clients = models.IntegerField(default=0)
    total_income_items = models.IntegerField(default=0)
    total_assets = models.IntegerField(default=0)
    total_liabilities = models.IntegerField(default=0)
    total_client_asset_types = models.IntegerField(default=0)
    total_documents = models.IntegerField(default=0)


class RiskAssessment(models.Model):
    submission = models.OneToOneField(SMISubmission, on_delete=models.CASCADE, related_name='risk_assessment')

    credit_risk_weight = models.DecimalField(max_digits=6, decimal_places=3, default=0)
    credit_risk_score = models.DecimalField(max_digits=6, decimal_places=3, default=0)
    credit_risk_rating = models.CharField(max_length=32, default='Not Calculated')

    market_risk_weight = models.DecimalField(max_digits=6, decimal_places=3, default=0)
    market_risk_score = models.DecimalField(max_digits=6, decimal_places=3, default=0)
    market_risk_rating = models.CharField(max_length=32, default='Not Calculated')

    liquidity_risk_weight = models.DecimalField(max_digits=6, decimal_places=3, default=0)
    liquidity_risk_score = models.DecimalField(max_digits=6, decimal_places=3, default=0)
    liquidity_risk_rating = models.CharField(max_length=32, default='Not Calculated')

    operational_risk_weight = models.DecimalField(max_digits=6, decimal_places=3, default=0)
    operational_risk_score = models.DecimalField(max_digits=6, decimal_places=3, default=0)
    operational_risk_rating = models.CharField(max_length=32, default='Not Calculated')

    legal_risk_weight = models.DecimalField(max_digits=6, decimal_places=3, default=0)
    legal_risk_score = models.DecimalField(max_digits=6, decimal_places=3, default=0)
    legal_risk_rating = models.CharField(max_length=32, default='Not Calculated')

    compliance_risk_weight = models.DecimalField(max_digits=6, decimal_places=3, default=0)
    compliance_risk_score = models.DecimalField(max_digits=6, decimal_places=3, default=0)
    compliance_risk_rating = models.CharField(max_length=32, default='Not Calculated')

    strategic_risk_weight = models.DecimalField(max_digits=6, decimal_places=3, default=0)
    strategic_risk_score = models.DecimalField(max_digits=6, decimal_places=3, default=0)
    strategic_risk_rating = models.CharField(max_length=32, default='Not Calculated')

    reputation_risk_weight = models.DecimalField(max_digits=6, decimal_places=3, default=0)
    reputation_risk_score = models.DecimalField(max_digits=6, decimal_places=3, default=0)
    reputation_risk_rating = models.CharField(max_length=32, default='Not Calculated')

    composite_risk_rating = models.CharField(max_length=32, default='Not Calculated')
    fsi_score = models.DecimalField(max_digits=6, decimal_places=3, default=0)

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)



