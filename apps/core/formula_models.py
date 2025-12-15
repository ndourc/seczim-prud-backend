from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import uuid


class CalculationFormula(models.Model):
    """
    Stores calculation formulae for risk metrics and other computed values.
    Allows admins to update formulae without code changes.
    """
    FORMULA_TYPES = [
        ('FSI_SCORE', 'Financial Stability Index Score'),
        ('CAR', 'Capital Adequacy Ratio'),
        ('CREDIT_RISK', 'Credit Risk'),
        ('MARKET_RISK', 'Market Risk'),
        ('LIQUIDITY_RISK', 'Liquidity Risk'),
        ('OPERATIONAL_RISK', 'Operational Risk'),
        ('LEGAL_RISK', 'Legal Risk'),
        ('COMPLIANCE_RISK', 'Compliance Risk'),
        ('STRATEGIC_RISK', 'Strategic Risk'),
        ('REPUTATION_RISK', 'Reputation Risk'),
        ('COMPOSITE_RISK', 'Composite Risk Rating'),
        ('COMPLIANCE_SCORE', 'Compliance Score'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    formula_type = models.CharField(max_length=50, choices=FORMULA_TYPES, unique=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    
    # Formula components
    formula_expression = models.TextField(
        help_text="Python expression for the formula. Available variables depend on formula type."
    )
    variables = models.JSONField(
        default=dict,
        help_text="Dictionary of variable names and their descriptions"
    )
    weights = models.JSONField(
        default=dict,
        help_text="Dictionary of weights for different components"
    )
    thresholds = models.JSONField(
        default=dict,
        help_text="Dictionary of threshold values for risk levels"
    )
    
    # Metadata
    is_active = models.BooleanField(default=True)
    version = models.IntegerField(default=1)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_formulas')
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='updated_formulas')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Audit trail
    change_notes = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.get_formula_type_display()} (v{self.version})"
    
    class Meta:
        verbose_name = "Calculation Formula"
        verbose_name_plural = "Calculation Formulae"
        ordering = ['formula_type', '-version']


class CalculationBreakdown(models.Model):
    """
    Stores the breakdown of how a calculated value was computed.
    Shows contributing factors and their impact on the final result.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Reference to what was calculated
    calculation_type = models.CharField(max_length=50)
    reference_id = models.UUIDField(help_text="ID of the related entity (SMI, RiskAssessment, etc.)")
    
    # Formula used
    formula = models.ForeignKey(CalculationFormula, on_delete=models.SET_NULL, null=True)
    
    # Results
    final_value = models.DecimalField(max_digits=10, decimal_places=4)
    final_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    
    # Breakdown of contributing factors
    components = models.JSONField(
        default=list,
        help_text="List of components with their values and impact percentages"
    )
    
    # Example structure for components:
    # [
    #     {
    #         "name": "Profit Margin",
    #         "value": 0.15,
    #         "weight": 0.6,
    #         "contribution": 0.09,
    #         "impact_percentage": 60.0,
    #         "description": "Company's profit margin ratio"
    #     },
    #     {
    #         "name": "Gross Margin",
    #         "value": 0.25,
    #         "weight": 0.4,
    #         "contribution": 0.10,
    #         "impact_percentage": 40.0,
    #         "description": "Company's gross margin ratio"
    #     }
    # ]
    
    # Metadata
    calculated_at = models.DateTimeField(default=timezone.now)
    calculated_by = models.CharField(max_length=100, default='system')
    
    def __str__(self):
        return f"{self.calculation_type} - {self.final_value} ({self.calculated_at.strftime('%Y-%m-%d')})"
    
    class Meta:
        verbose_name = "Calculation Breakdown"
        verbose_name_plural = "Calculation Breakdowns"
        ordering = ['-calculated_at']
        indexes = [
            models.Index(fields=['calculation_type', 'reference_id']),
            models.Index(fields=['-calculated_at']),
        ]
