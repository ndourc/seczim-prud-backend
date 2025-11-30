from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from apps.core.models import SMI
import uuid

class LicensingPortalIntegration(models.Model):
    """Integration with existing licensing portal API"""
    INTEGRATION_STATUS = [
        ('ACTIVE', 'Active'),
        ('INACTIVE', 'Inactive'),
        ('ERROR', 'Error'),
        ('MAINTENANCE', 'Under Maintenance')
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    portal_name = models.CharField(max_length=255, default='Licensing Portal')
    api_endpoint = models.URLField(default='https://api.licensing-portal.com')
    api_key = models.CharField(max_length=255, blank=True)
    
    # Integration Status
    status = models.CharField(max_length=20, choices=INTEGRATION_STATUS, default='ACTIVE')
    last_sync = models.DateTimeField(null=True, blank=True)
    sync_frequency = models.CharField(max_length=20, choices=[
        ('HOURLY', 'Hourly'),
        ('DAILY', 'Daily'),
        ('WEEKLY', 'Weekly'),
        ('MANUAL', 'Manual')
    ], default='DAILY')
    
    # Configuration
    auto_sync_enabled = models.BooleanField(default=True)
    sync_errors = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.portal_name} - {self.status}"

class PortalSMIData(models.Model):
    """SMI data fetched from licensing portal"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    smi = models.OneToOneField(SMI, on_delete=models.CASCADE, related_name='portal_data')
    
    # Portal Data
    portal_id = models.CharField(max_length=100, unique=True)
    portal_status = models.CharField(max_length=50, default='Active')
    last_updated_from_portal = models.DateTimeField(auto_now=True)
    
    # Financial Data from Portal
    portal_capital_adequacy = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    portal_licensing_fee = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    portal_annual_revenue = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    
    # Portal Metadata
    portal_created_date = models.DateField(null=True, blank=True)
    portal_last_review_date = models.DateField(null=True, blank=True)
    portal_next_review_date = models.DateField(null=True, blank=True)
    
    # Sync Information
    sync_status = models.CharField(max_length=20, choices=[
        ('SYNCED', 'Synced'),
        ('PENDING', 'Pending'),
        ('FAILED', 'Failed'),
        ('OUTDATED', 'Outdated')
    ], default='PENDING')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Portal Data - {self.smi.company_name}"

class InstitutionalProfile(models.Model):
    """Enhanced institutional profiling data"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    smi = models.OneToOneField(SMI, on_delete=models.CASCADE, related_name='institutional_profile')
    
    # Business Profile
    business_model = models.TextField(default='Business model to be described')
    target_markets = models.JSONField(default=list, help_text="List of target markets")
    competitive_position = models.CharField(max_length=100, choices=[
        ('MARKET_LEADER', 'Market Leader'),
        ('MAJOR_PLAYER', 'Major Player'),
        ('MID_TIER', 'Mid-tier'),
        ('SMALL_PLAYER', 'Small Player'),
        ('NICHE', 'Niche Player')
    ], default='MID_TIER')
    
    # Financial Profile
    credit_rating = models.CharField(max_length=10, blank=True)
    debt_rating = models.CharField(max_length=10, blank=True)
    financial_strength = models.CharField(max_length=20, choices=[
        ('EXCELLENT', 'Excellent'),
        ('GOOD', 'Good'),
        ('SATISFACTORY', 'Satisfactory'),
        ('WEAK', 'Weak'),
        ('POOR', 'Poor')
    ], default='SATISFACTORY')
    
    # Risk Profile
    risk_appetite = models.CharField(max_length=20, choices=[
        ('CONSERVATIVE', 'Conservative'),
        ('MODERATE', 'Moderate'),
        ('AGGRESSIVE', 'Aggressive'),
        ('VERY_AGGRESSIVE', 'Very Aggressive')
    ], default='MODERATE')
    
    # Operational Profile
    number_of_employees = models.IntegerField(default=0)
    number_of_branches = models.IntegerField(default=0)
    operating_countries = models.JSONField(default=list)
    
    # Compliance Profile
    compliance_history = models.TextField(blank=True)
    regulatory_relationships = models.JSONField(default=list)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Institutional Profile - {self.smi.company_name}"

    class Meta:
        ordering = ['-created_at']

class Shareholder(models.Model):
    """Shareholder information for SMIs"""
    SHAREHOLDER_TYPES = [
        ('INDIVIDUAL', 'Individual'),
        ('CORPORATE', 'Corporate'),
        ('GOVERNMENT', 'Government'),
        ('INSTITUTIONAL', 'Institutional'),
        ('FOREIGN', 'Foreign Entity')
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    smi = models.ForeignKey(SMI, on_delete=models.CASCADE, related_name='shareholders')
    
    # Shareholder Details
    name = models.CharField(max_length=255)
    shareholder_type = models.CharField(max_length=20, choices=SHAREHOLDER_TYPES, default='INDIVIDUAL')
    nationality = models.CharField(max_length=100, blank=True)
    
    # Ownership Details
    ownership_percentage = models.DecimalField(max_digits=5, decimal_places=2, 
                                            validators=[MinValueValidator(0), MaxValueValidator(100)])
    shares_held = models.IntegerField(default=0)
    voting_rights = models.BooleanField(default=True)
    
    # Financial Details
    investment_amount = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    investment_date = models.DateField(null=True, blank=True)
    
    # Regulatory Information
    regulatory_approval = models.BooleanField(default=False)
    approval_date = models.DateField(null=True, blank=True)
    approval_reference = models.CharField(max_length=255, blank=True)
    
    # Status
    is_active = models.BooleanField(default=True)
    notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.smi.company_name} ({self.ownership_percentage}%)"

    class Meta:
        ordering = ['-ownership_percentage']

class Director(models.Model):
    """Director and key personnel information"""
    DIRECTOR_TYPES = [
        ('EXECUTIVE', 'Executive Director'),
        ('NON_EXECUTIVE', 'Non-Executive Director'),
        ('INDEPENDENT', 'Independent Director'),
        ('CHAIRMAN', 'Chairman'),
        ('CEO', 'Chief Executive Officer'),
        ('CFO', 'Chief Financial Officer'),
        ('COO', 'Chief Operating Officer'),
        ('CRO', 'Chief Risk Officer'),
        ('CCO', 'Chief Compliance Officer')
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    smi = models.ForeignKey(SMI, on_delete=models.CASCADE, related_name='directors')
    
    # Personal Details
    name = models.CharField(max_length=255)
    director_type = models.CharField(max_length=20, choices=DIRECTOR_TYPES, default='EXECUTIVE')
    nationality = models.CharField(max_length=100, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    
    # Professional Details
    qualifications = models.TextField(blank=True)
    experience_years = models.IntegerField(default=0)
    previous_positions = models.JSONField(default=list)
    
    # Appointment Details
    appointment_date = models.DateField()
    resignation_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    
    # Regulatory Information
    regulatory_approval = models.BooleanField(default=False)
    approval_date = models.DateField(null=True, blank=True)
    fit_and_proper_assessment = models.CharField(max_length=20, choices=[
        ('PASSED', 'Passed'),
        ('FAILED', 'Failed'),
        ('PENDING', 'Pending'),
        ('NOT_ASSESSED', 'Not Assessed')
    ], default='NOT_ASSESSED')
    
    # Compliance
    training_completed = models.BooleanField(default=False)
    last_training_date = models.DateField(null=True, blank=True)
    compliance_status = models.CharField(max_length=20, choices=[
        ('COMPLIANT', 'Compliant'),
        ('NON_COMPLIANT', 'Non-Compliant'),
        ('UNDER_REVIEW', 'Under Review')
    ], default='UNDER_REVIEW')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.director_type} at {self.smi.company_name}"

    class Meta:
        ordering = ['appointment_date']

class LicenseHistory(models.Model):
    """License history and changes tracking"""
    CHANGE_TYPES = [
        ('GRANTED', 'License Granted'),
        ('RENEWED', 'License Renewed'),
        ('AMENDED', 'License Amended'),
        ('SUSPENDED', 'License Suspended'),
        ('REVOKED', 'License Revoked'),
        ('RESTORED', 'License Restored'),
        ('EXPIRED', 'License Expired')
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    smi = models.ForeignKey(SMI, on_delete=models.CASCADE, related_name='license_history')
    
    # Change Details
    change_type = models.CharField(max_length=20, choices=CHANGE_TYPES, default='GRANTED')
    change_date = models.DateField()
    effective_date = models.DateField()
    
    # License Details
    license_number = models.CharField(max_length=100)
    license_type = models.CharField(max_length=100)
    license_scope = models.TextField()
    license_conditions = models.JSONField(default=list)
    
    # Regulatory Information
    regulatory_authority = models.CharField(max_length=255)
    approval_reference = models.CharField(max_length=255, blank=True)
    regulatory_officer = models.CharField(max_length=255, blank=True)
    
    # Financial Information
    license_fee = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    security_deposit = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    
    # Timeline
    expiry_date = models.DateField(null=True, blank=True)
    renewal_due_date = models.DateField(null=True, blank=True)
    
    # Status
    is_active = models.BooleanField(default=True)
    notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.change_type} - {self.smi.company_name} - {self.change_date}"

    class Meta:
        ordering = ['-change_date']
