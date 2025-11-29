from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from apps.core.models import SMI
import uuid

class VA_VASP(models.Model):
    """Virtual Assets and Virtual Asset Service Providers analysis"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    smi = models.ForeignKey(SMI, on_delete=models.CASCADE, related_name='va_vasp_analyses')
    analysis_date = models.DateField(default=timezone.now)
    
    # VA/VASP Classification
    is_va_issuer = models.BooleanField(default=False)
    is_vasp = models.BooleanField(default=False)
    va_types = models.TextField(blank=True, help_text="Types of virtual assets handled")
    
    # Risk Assessment
    va_risk_score = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(100)], default=50)
    vasp_risk_score = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(100)], default=50)
    overall_va_risk_score = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(100)], default=50)
    
    # Securities Sector Specific
    securities_exposure = models.DecimalField(max_digits=5, decimal_places=2, 
                                           validators=[MinValueValidator(0), MaxValueValidator(100)], default=0)
    regulatory_compliance = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(100)], default=75)
    
    # Risk Profile Outputs
    risk_profile = models.TextField(default='Risk profile to be generated')
    recommendations = models.TextField(default='Recommendations to be provided')
    
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"VA/VASP Analysis - {self.smi.company_name} - {self.analysis_date}"

    class Meta:
        ordering = ['-analysis_date']

    def calculate_overall_va_risk_score(self):
        """Calculate overall VA risk score"""
        if self.is_va_issuer and self.is_vasp:
            # Both VA issuer and VASP - higher risk
            self.overall_va_risk_score = (self.va_risk_score * 0.4 + self.vasp_risk_score * 0.6)
        elif self.is_va_issuer:
            # Only VA issuer
            self.overall_va_risk_score = self.va_risk_score
        elif self.is_vasp:
            # Only VASP
            self.overall_va_risk_score = self.vasp_risk_score
        else:
            # Neither - lowest risk
            self.overall_va_risk_score = 0
        
        return round(self.overall_va_risk_score, 2)

class VirtualAsset(models.Model):
    """Virtual asset types and characteristics"""
    ASSET_CATEGORIES = [
        ('CRYPTO', 'Cryptocurrency'),
        ('TOKEN', 'Token'),
        ('NFT', 'Non-Fungible Token'),
        ('STABLECOIN', 'Stablecoin'),
        ('DEFI_TOKEN', 'DeFi Token'),
        ('GAMING_TOKEN', 'Gaming Token'),
        ('OTHER', 'Other')
    ]
    
    RISK_LEVELS = [
        ('LOW', 'Low Risk'),
        ('MEDIUM', 'Medium Risk'),
        ('HIGH', 'High Risk'),
        ('CRITICAL', 'Critical Risk')
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    va_vasp_analysis = models.ForeignKey(VA_VASP, on_delete=models.CASCADE, related_name='virtual_assets')
    asset_name = models.CharField(max_length=255)
    asset_symbol = models.CharField(max_length=20)
    asset_category = models.CharField(max_length=20, choices=ASSET_CATEGORIES, default='OTHER')
    
    # Asset Characteristics
    market_cap = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    trading_volume = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    volatility_index = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(100)], null=True, blank=True)
    
    # Risk Assessment
    risk_level = models.CharField(max_length=20, choices=RISK_LEVELS, default='MEDIUM')
    risk_score = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(100)], default=50)
    risk_factors = models.TextField(blank=True, help_text="Key risk factors identified")
    
    # Regulatory Status
    regulatory_status = models.CharField(max_length=50, default='Under Review')
    compliance_requirements = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.asset_name} ({self.asset_symbol}) - {self.va_vasp_analysis.smi.company_name}"

class VASPService(models.Model):
    """Virtual Asset Service Provider services and activities"""
    SERVICE_TYPES = [
        ('EXCHANGE', 'Exchange Service'),
        ('WALLET', 'Wallet Service'),
        ('TRANSFER', 'Transfer Service'),
        ('CUSTODY', 'Custody Service'),
        ('TRADING', 'Trading Service'),
        ('STAKING', 'Staking Service'),
        ('LENDING', 'Lending Service'),
        ('OTHER', 'Other Service')
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    va_vasp_analysis = models.ForeignKey(VA_VASP, on_delete=models.CASCADE, related_name='vasp_services')
    service_type = models.CharField(max_length=20, choices=SERVICE_TYPES, default='OTHER')
    service_name = models.CharField(max_length=255)
    service_description = models.TextField(blank=True)
    
    # Service Characteristics
    is_active = models.BooleanField(default=True)
    customer_count = models.IntegerField(default=0)
    transaction_volume = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    
    # Risk Assessment
    service_risk_score = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(100)], default=50)
    risk_mitigation_measures = models.TextField(blank=True)
    
    # Compliance
    regulatory_licenses = models.TextField(blank=True)
    compliance_status = models.CharField(max_length=50, default='Under Review')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.service_name} - {self.va_vasp_analysis.smi.company_name}"

class VARiskAssessment(models.Model):
    """Detailed risk assessment for virtual assets"""
    RISK_CATEGORIES = [
        ('MARKET_RISK', 'Market Risk'),
        ('LIQUIDITY_RISK', 'Liquidity Risk'),
        ('OPERATIONAL_RISK', 'Operational Risk'),
        ('REGULATORY_RISK', 'Regulatory Risk'),
        ('TECHNOLOGY_RISK', 'Technology Risk'),
        ('CYBERSECURITY_RISK', 'Cybersecurity Risk'),
        ('COMPLIANCE_RISK', 'Compliance Risk')
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    va_vasp_analysis = models.ForeignKey(VA_VASP, on_delete=models.CASCADE, related_name='va_risk_assessments')
    risk_category = models.CharField(max_length=30, choices=RISK_CATEGORIES, default='MARKET_RISK')
    
    # Risk Metrics
    risk_score = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(100)], default=50)
    risk_probability = models.CharField(max_length=20, choices=[
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High'),
        ('VERY_HIGH', 'Very High')
    ], default='MEDIUM')
    
    risk_impact = models.CharField(max_length=20, choices=[
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High'),
        ('CRITICAL', 'Critical')
    ], default='MEDIUM')
    
    # Risk Details
    risk_description = models.TextField(blank=True)
    risk_factors = models.TextField(blank=True)
    mitigation_strategies = models.TextField(blank=True)
    
    # Assessment
    assessment_date = models.DateField(default=timezone.now)
    assessor_notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.risk_category} - {self.va_vasp_analysis.smi.company_name}"

    class Meta:
        ordering = ['-assessment_date']

class VASPCompliance(models.Model):
    """Compliance tracking for VASP activities"""
    COMPLIANCE_AREAS = [
        ('KYC_AML', 'KYC/AML Compliance'),
        ('LICENSING', 'Licensing Requirements'),
        ('REPORTING', 'Reporting Requirements'),
        ('CAPITAL_ADEQUACY', 'Capital Adequacy'),
        ('CUSTODY', 'Custody Requirements'),
        ('CONSUMER_PROTECTION', 'Consumer Protection'),
        ('DATA_PROTECTION', 'Data Protection'),
        ('OTHER', 'Other Requirements')
    ]
    
    COMPLIANCE_STATUS = [
        ('COMPLIANT', 'Compliant'),
        ('NON_COMPLIANT', 'Non-Compliant'),
        ('PARTIALLY_COMPLIANT', 'Partially Compliant'),
        ('UNDER_REVIEW', 'Under Review'),
        ('PENDING', 'Pending')
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    va_vasp_analysis = models.ForeignKey(VA_VASP, on_delete=models.CASCADE, related_name='vasp_compliance')
    compliance_area = models.CharField(max_length=30, choices=COMPLIANCE_AREAS, default='OTHER')
    
    # Compliance Details
    compliance_status = models.CharField(max_length=30, choices=COMPLIANCE_STATUS, default='UNDER_REVIEW')
    compliance_score = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(100)], default=0)
    
    # Requirements and Assessment
    requirements = models.TextField(blank=True)
    current_status = models.TextField(blank=True)
    gaps_identified = models.TextField(blank=True)
    remediation_plan = models.TextField(blank=True)
    
    # Timeline
    assessment_date = models.DateField(default=timezone.now)
    target_compliance_date = models.DateField(null=True, blank=True)
    actual_compliance_date = models.DateField(null=True, blank=True)
    
    # Follow-up
    follow_up_required = models.BooleanField(default=False)
    follow_up_date = models.DateField(null=True, blank=True)
    follow_up_notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.compliance_area} - {self.va_vasp_analysis.smi.company_name}"

    class Meta:
        ordering = ['-assessment_date']
