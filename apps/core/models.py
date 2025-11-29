from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid

class SMI(models.Model):
    """Supervised Market Intermediary - Core entity"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company_name = models.CharField(max_length=255)
    license_number = models.CharField(max_length=100, unique=True)
    registration_date = models.DateField(default=timezone.localdate)
    business_type = models.CharField(max_length=100, default='Financial Services')
    address = models.TextField(default='Address to be provided')
    phone = models.CharField(max_length=20, default='Phone to be provided')
    email = models.EmailField(default='email@example.com')
    website = models.URLField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=[
        ('ACTIVE', 'Active'),
        ('SUSPENDED', 'Suspended'),
        ('CANCELLED', 'Cancelled'),
        ('PENDING', 'Pending Review')
    ], default='ACTIVE')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.company_name} ({self.license_number})"

    class Meta:
        verbose_name = "SMI"
        verbose_name_plural = "SMIs"
        ordering = ['company_name']

class BoardMember(models.Model):
    """Board and Management Committee members"""
    smi = models.ForeignKey(SMI, on_delete=models.CASCADE, related_name='board_members')
    name = models.CharField(max_length=255)
    position = models.CharField(max_length=100)
    appointment_date = models.DateField()
    resignation_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.name} - {self.position} at {self.smi.company_name}"

class MeetingLog(models.Model):
    """Board and Management Committee meeting logs"""
    smi = models.ForeignKey(SMI, on_delete=models.CASCADE, related_name='meeting_logs')
    meeting_date = models.DateField()
    meeting_type = models.CharField(max_length=50, choices=[
        ('BOARD', 'Board Meeting'),
        ('MANAGEMENT', 'Management Meeting'),
        ('AUDIT', 'Audit Committee'),
        ('RISK', 'Risk Committee')
    ])
    attendees = models.TextField()
    agenda = models.TextField()
    decisions = models.TextField()
    action_items = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.meeting_type} - {self.smi.company_name} - {self.meeting_date}"

class ProductOffering(models.Model):
    """Product offerings and income contribution"""
    smi = models.ForeignKey(SMI, on_delete=models.CASCADE, related_name='product_offerings')
    product_name = models.CharField(max_length=255)
    product_category = models.CharField(max_length=100)
    income_contribution = models.DecimalField(max_digits=5, decimal_places=2, 
                                           validators=[MinValueValidator(0), MaxValueValidator(100)])
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.product_name} - {self.smi.company_name}"

class ClienteleProfile(models.Model):
    """Client profile and income contribution"""
    smi = models.ForeignKey(SMI, on_delete=models.CASCADE, related_name='clientele_profiles')
    client_type = models.CharField(max_length=100, choices=[
        ('RETAIL', 'Retail'),
        ('WHOLESALE', 'Wholesale'),
        ('INSTITUTIONAL', 'Institutional'),
        ('CORPORATE', 'Corporate')
    ])
    client_count = models.IntegerField()
    income_contribution = models.DecimalField(max_digits=5, decimal_places=2,
                                           validators=[MinValueValidator(0), MaxValueValidator(100)])
    period = models.DateField(default=timezone.now)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.client_type} - {self.smi.company_name} - {self.period}"

class FinancialStatement(models.Model):
    """Comprehensive financial statements"""
    smi = models.ForeignKey(SMI, on_delete=models.CASCADE, related_name='financial_statements')
    period = models.DateField()
    statement_type = models.CharField(max_length=50, choices=[
        ('COMPREHENSIVE_INCOME', 'Comprehensive Income'),
        ('FINANCIAL_POSITION', 'Financial Position'),
        ('CASH_FLOW', 'Cash Flow')
    ], default='FINANCIAL_POSITION')
    
    # Income Statement
    total_revenue = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    total_expenses = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    profit_before_tax = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    net_profit = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    
    # Balance Sheet
    total_assets = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    total_liabilities = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    total_equity = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    
    # Ratios
    gross_margin = models.FloatField(null=True, blank=True)
    profit_margin = models.FloatField(null=True, blank=True)
    debt_to_equity = models.FloatField(null=True, blank=True)
    
    file_upload = models.FileField(upload_to='financial_statements/', null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.statement_type} - {self.smi.company_name} - {self.period}"

    class Meta:
        unique_together = ['smi', 'period', 'statement_type']

class ClientAssetMix(models.Model):
    """Clients' asset mix and net capital position"""
    smi = models.ForeignKey(SMI, on_delete=models.CASCADE, related_name='client_asset_mixes')
    period = models.DateField(default=timezone.now)
    asset_class = models.CharField(max_length=100, choices=[
        ('EQUITIES', 'Equities'),
        ('FIXED_INCOME', 'Fixed Income'),
        ('ALTERNATIVES', 'Alternatives'),
        ('CASH', 'Cash & Equivalents'),
        ('REAL_ESTATE', 'Real Estate'),
        ('COMMODITIES', 'Commodities')
    ], default='EQUITIES')
    allocation_percentage = models.DecimalField(max_digits=5, decimal_places=2,
                                             validators=[MinValueValidator(0), MaxValueValidator(100)], default=0)
    market_value = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    net_capital_position = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    sec_compliance_status = models.CharField(max_length=20, choices=[
        ('COMPLIANT', 'Compliant'),
        ('NON_COMPLIANT', 'Non-Compliant'),
        ('UNDER_REVIEW', 'Under Review')
    ], default='COMPLIANT')
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.asset_class} - {self.smi.company_name} - {self.period}"



class LicensingBreach(models.Model):
    """Licensing breaches, cancellations, and suspensions"""
    BREACH_TYPES = [
        ('MINOR', 'Minor Breach'),
        ('MAJOR', 'Major Breach'),
        ('CRITICAL', 'Critical Breach'),
        ('CANCELLATION', 'License Cancellation'),
        ('SUSPENSION', 'License Suspension')
    ]
    
    STATUS_CHOICES = [
        ('OPEN', 'Open'),
        ('INVESTIGATING', 'Investigating'),
        ('RESOLVED', 'Resolved'),
        ('ESCALATED', 'Escalated'),
        ('CLOSED', 'Closed')
    ]
    
    smi = models.ForeignKey(SMI, on_delete=models.CASCADE, related_name='licensing_breaches')
    breach_type = models.CharField(max_length=20, choices=BREACH_TYPES, default='MINOR')
    breach_date = models.DateField(default=timezone.now)
    description = models.TextField(default='Breach description to be provided')
    regulatory_reference = models.CharField(max_length=255, help_text="Regulatory provision violated", default='Regulatory reference to be specified')
    
    # Investigation
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='OPEN')
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    investigation_notes = models.TextField(blank=True)
    
    # Resolution
    resolution_date = models.DateField(null=True, blank=True)
    resolution_action = models.TextField(blank=True)
    penalty_amount = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.breach_type} - {self.smi.company_name} - {self.breach_date}"

class SupervisoryIntervention(models.Model):
    """Log of supervisory interventions"""
    INTERVENTION_TYPES = [
        ('WARNING', 'Warning Letter'),
        ('FINE', 'Monetary Fine'),
        ('SUSPENSION', 'Temporary Suspension'),
        ('RESTRICTION', 'Business Restriction'),
        ('REQUIREMENT', 'Additional Requirements'),
        ('ENHANCED_MONITORING', 'Enhanced Monitoring')
    ]
    
    smi = models.ForeignKey(SMI, on_delete=models.CASCADE, related_name='supervisory_interventions')
    intervention_type = models.CharField(max_length=30, choices=INTERVENTION_TYPES, default='WARNING')
    intervention_date = models.DateField(default=timezone.now)
    reason = models.TextField(default='Intervention reason to be specified')
    description = models.TextField(default='Intervention description to be provided')
    
    # Intensity and Frequency
    intensity = models.CharField(max_length=20, choices=[
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High'),
        ('CRITICAL', 'Critical')
    ], default='MEDIUM')
    frequency = models.CharField(max_length=20, choices=[
        ('ONE_TIME', 'One Time'),
        ('RECURRING', 'Recurring'),
        ('CONTINUOUS', 'Continuous')
    ], default='ONE_TIME')
    
    # Follow-up
    follow_up_required = models.BooleanField(default=False)
    follow_up_date = models.DateField(null=True, blank=True)
    outcome = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.intervention_type} - {self.smi.company_name} - {self.intervention_date}"



class Notification(models.Model):
    """System notifications and alerts"""
    NOTIFICATION_TYPES = [
        ('LICENSING_UPDATE', 'Licensing Portal Update'),
        ('MARKET_SUBMISSION', 'Market Submission'),
        ('TRAINING_VIDEO', 'New Training Video'),
        ('MATERIAL_UPLOAD', 'New Material Uploaded'),
        ('RISK_THRESHOLD', 'Risk Threshold Alert'),
        ('MANAGEMENT_CHANGE', 'Management Change Alert'),
        ('BUSINESS_ACTIVITY', 'Business Activity Change'),
        ('INSPECTION_DUE', 'Inspection Due'),
        ('COMPLIANCE_DEADLINE', 'Compliance Deadline'),
        ('BREACH_ALERT', 'Breach Alert')
    ]
    
    PRIORITY_CHOICES = [
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High'),
        ('URGENT', 'Urgent')
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=30, choices=NOTIFICATION_TYPES, default='MARKET_SUBMISSION')
    title = models.CharField(max_length=255, default='Notification title')
    message = models.TextField(default='Notification message')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='MEDIUM')
    
    # Content and Links
    content_link = models.URLField(blank=True, null=True)
    related_entity_type = models.CharField(max_length=50, blank=True)
    related_entity_id = models.UUIDField(null=True, blank=True)
    
    # Status
    read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)
    
    # Delivery
    email_sent = models.BooleanField(default=False)
    email_sent_at = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.notification_type} - {self.user.username} - {self.created_at.strftime('%Y-%m-%d')}"

    class Meta:
        ordering = ['-created_at']

class SystemAuditLog(models.Model):
    """Audit trail for all system activities"""
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    action = models.CharField(max_length=100, default='Unknown action')
    model_name = models.CharField(max_length=100, default='Unknown model')
    object_id = models.CharField(max_length=100, default='Unknown ID')
    object_repr = models.CharField(max_length=255, default='Unknown object')
    change_message = models.TextField(default='Change message to be provided')
    timestamp = models.DateTimeField(default=timezone.now)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)

    def __str__(self):
        return f"{self.action} by {self.user} on {self.model_name} at {self.timestamp}"

    class Meta:
        ordering = ['-timestamp']