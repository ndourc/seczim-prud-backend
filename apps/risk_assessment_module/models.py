from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from apps.core.models import SMI
import uuid

class RiskAssessment(models.Model):
    """Comprehensive risk assessment and scoring"""
    RISK_LEVELS = [
        ('LOW', 'Low Risk'),
        ('MEDIUM_LOW', 'Medium-Low Risk'),
        ('MEDIUM', 'Medium Risk'),
        ('MEDIUM_HIGH', 'Medium-High Risk'),
        ('HIGH', 'High Risk'),
        ('CRITICAL', 'Critical Risk'),
    ]
    
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
        ('REVIEW_REQUIRED', 'Review Required'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    smi = models.ForeignKey(SMI, on_delete=models.CASCADE, related_name='risk_assessments')
    assessment_date = models.DateField(default=timezone.now)
    assessment_period = models.CharField(max_length=20, choices=[
        ('QUARTERLY', 'Quarterly'),
        ('ANNUAL', 'Annual'),
        ('AD_HOC', 'Ad-hoc')
    ], default='QUARTERLY')
    
    # Risk Scores
    fsi_score = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(100)], default=50)
    inherent_risk_score = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(100)], default=50)
    operational_risk_score = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(100)], default=50)
    market_risk_score = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(100)], default=50)
    credit_risk_score = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(100)], default=50)
    
    # Financial Ratios
    car = models.FloatField(help_text="Capital Adequacy Ratio", default=15)
    liquidity_ratio = models.FloatField(null=True, blank=True)
    leverage_ratio = models.FloatField(null=True, blank=True)
    
    # Overall Assessment
    risk_level = models.CharField(max_length=20, choices=RISK_LEVELS, default='MEDIUM')
    compliance_score = models.FloatField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    overall_risk_score = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(100)], default=50)
    
    # Status and Metadata
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    assessor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Risk Assessment - {self.smi.company_name} - {self.assessment_date}"

    class Meta:
        unique_together = ['smi', 'assessment_date', 'assessment_period']
        ordering = ['-assessment_date']

    def calculate_overall_risk_score(self):
        """Calculate overall risk score based on component scores"""
        weights = {
            'fsi': 0.25,
            'inherent': 0.20,
            'operational': 0.20,
            'market': 0.15,
            'credit': 0.20
        }
        
        overall_score = (
            self.fsi_score * weights['fsi'] +
            self.inherent_risk_score * weights['inherent'] +
            self.operational_risk_score * weights['operational'] +
            self.market_risk_score * weights['market'] +
            self.credit_risk_score * weights['credit']
        )
        
        self.overall_risk_score = round(overall_score, 2)
        return self.overall_risk_score

    def determine_risk_level(self):
        """Determine risk level based on overall score"""
        if self.overall_risk_score <= 20:
            self.risk_level = 'LOW'
        elif self.overall_risk_score <= 40:
            self.risk_level = 'MEDIUM_LOW'
        elif self.overall_risk_score <= 60:
            self.risk_level = 'MEDIUM'
        elif self.overall_risk_score <= 80:
            self.risk_level = 'MEDIUM_HIGH'
        elif self.overall_risk_score <= 90:
            self.risk_level = 'HIGH'
        else:
            self.risk_level = 'CRITICAL'
        
        return self.risk_level

class StressTest(models.Model):
    """Stress testing results for SMI and industry"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    smi = models.ForeignKey(SMI, on_delete=models.CASCADE, related_name='stress_tests', null=True, blank=True)
    test_date = models.DateField(default=timezone.localdate)
    test_type = models.CharField(max_length=50, choices=[
        ('SMI_LEVEL', 'SMI Level'),
        ('INDUSTRY_LEVEL', 'Industry Level'),
        ('SCENARIO', 'Scenario Based')
    ], default='SMI_LEVEL')
    scenario_name = models.CharField(max_length=255, default='Default Scenario')
    scenario_description = models.TextField(default='Scenario description to be provided')
    
    # Test Results
    capital_adequacy_impact = models.FloatField(help_text="Impact on CAR", default=0)
    liquidity_impact = models.FloatField(help_text="Impact on liquidity ratio", default=0)
    profitability_impact = models.FloatField(help_text="Impact on profitability", default=0)
    risk_score_change = models.FloatField(help_text="Change in risk score", default=0)
    
    # Pass/Fail
    passed = models.BooleanField(default=False)
    threshold_breach = models.BooleanField(default=False)
    recommendations = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Stress Test - {self.scenario_name} - {self.test_date}"

class RiskIndicator(models.Model):
    """Risk indicators and metrics for monitoring"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    smi = models.ForeignKey(SMI, on_delete=models.CASCADE, related_name='risk_indicators')
    indicator_date = models.DateField(default=timezone.now)
    indicator_type = models.CharField(max_length=50, choices=[
        ('FINANCIAL', 'Financial Indicator'),
        ('OPERATIONAL', 'Operational Indicator'),
        ('MARKET', 'Market Indicator'),
        ('REGULATORY', 'Regulatory Indicator')
    ])
    
    indicator_name = models.CharField(max_length=255)
    current_value = models.FloatField()
    threshold_value = models.FloatField()
    trend = models.CharField(max_length=20, choices=[
        ('IMPROVING', 'Improving'),
        ('STABLE', 'Stable'),
        ('DETERIORATING', 'Deteriorating'),
        ('CRITICAL', 'Critical')
    ], default='STABLE')
    
    is_breached = models.BooleanField(default=False)
    alert_level = models.CharField(max_length=20, choices=[
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High'),
        ('CRITICAL', 'Critical')
    ], default='LOW')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.indicator_name} - {self.smi.company_name} - {self.indicator_date}"

    class Meta:
        ordering = ['-indicator_date']

class RiskTrend(models.Model):
    """Risk trend analysis and performance tracking"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    smi = models.ForeignKey(SMI, on_delete=models.CASCADE, related_name='risk_trends')
    period_start = models.DateField()
    period_end = models.DateField()
    
    # Trend Metrics
    risk_score_change = models.FloatField(help_text="Change in risk score from previous period")
    risk_level_change = models.CharField(max_length=20, choices=[
        ('IMPROVED', 'Improved'),
        ('STABLE', 'Stable'),
        ('DETERIORATED', 'Deteriorated'),
        ('CRITICAL', 'Critical Deterioration')
    ], default='STABLE')
    
    # Performance Indicators
    financial_performance = models.CharField(max_length=20, choices=[
        ('POSITIVE', 'Positive'),
        ('NEUTRAL', 'Neutral'),
        ('NEGATIVE', 'Negative')
    ], default='NEUTRAL')
    
    compliance_performance = models.CharField(max_length=20, choices=[
        ('POSITIVE', 'Positive'),
        ('NEUTRAL', 'Neutral'),
        ('NEGATIVE', 'Negative')
    ], default='NEUTRAL')
    
    # Analysis
    key_factors = models.TextField(help_text="Key factors contributing to risk changes")
    recommendations = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Risk Trend - {self.smi.company_name} - {self.period_start} to {self.period_end}"

    class Meta:
        ordering = ['-period_start']
