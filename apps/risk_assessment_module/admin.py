from django.contrib import admin
from .models import RiskAssessment, StressTest, RiskIndicator, RiskTrend

@admin.register(RiskAssessment)
class RiskAssessmentAdmin(admin.ModelAdmin):
    list_display = ['smi', 'assessment_date', 'assessment_period', 'fsi_score', 'overall_risk_score', 'risk_level', 'status']
    list_filter = ['assessment_period', 'risk_level', 'status', 'assessment_date']
    search_fields = ['smi__company_name', 'assessor__username']
    readonly_fields = ['overall_risk_score', 'risk_level', 'created_at', 'updated_at']
    
    fieldsets = (
        ('SMI Information', {
            'fields': ('smi', 'assessment_date', 'assessment_period')
        }),
        ('Risk Scores', {
            'fields': ('fsi_score', 'inherent_risk_score', 'operational_risk_score', 'market_risk_score', 'credit_risk_score')
        }),
        ('Financial Ratios', {
            'fields': ('car', 'liquidity_ratio', 'leverage_ratio')
        }),
        ('Overall Assessment', {
            'fields': ('overall_risk_score', 'risk_level', 'compliance_score')
        }),
        ('Status and Metadata', {
            'fields': ('status', 'assessor', 'notes')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

@admin.register(StressTest)
class StressTestAdmin(admin.ModelAdmin):
    list_display = ['smi', 'test_date', 'test_type', 'scenario_name', 'passed', 'threshold_breach']
    list_filter = ['test_type', 'passed', 'threshold_breach', 'test_date']
    search_fields = ['scenario_name', 'smi__company_name']
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('Test Information', {
            'fields': ('smi', 'test_date', 'test_type', 'scenario_name', 'scenario_description')
        }),
        ('Test Results', {
            'fields': ('capital_adequacy_impact', 'liquidity_impact', 'profitability_impact', 'risk_score_change')
        }),
        ('Assessment', {
            'fields': ('passed', 'threshold_breach', 'recommendations')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        })
    )

@admin.register(RiskIndicator)
class RiskIndicatorAdmin(admin.ModelAdmin):
    list_display = ['smi', 'indicator_date', 'indicator_type', 'indicator_name', 'current_value', 'threshold_value', 'is_breached', 'alert_level']
    list_filter = ['indicator_type', 'trend', 'is_breached', 'alert_level', 'indicator_date']
    search_fields = ['indicator_name', 'smi__company_name']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Indicator Information', {
            'fields': ('smi', 'indicator_date', 'indicator_type', 'indicator_name')
        }),
        ('Values and Thresholds', {
            'fields': ('current_value', 'threshold_value', 'trend')
        }),
        ('Status', {
            'fields': ('is_breached', 'alert_level')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

@admin.register(RiskTrend)
class RiskTrendAdmin(admin.ModelAdmin):
    list_display = ['smi', 'period_start', 'period_end', 'risk_level_change', 'financial_performance', 'compliance_performance']
    list_filter = ['risk_level_change', 'financial_performance', 'compliance_performance', 'period_start']
    search_fields = ['smi__company_name', 'key_factors']
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('Period Information', {
            'fields': ('smi', 'period_start', 'period_end')
        }),
        ('Trend Metrics', {
            'fields': ('risk_score_change', 'risk_level_change')
        }),
        ('Performance Indicators', {
            'fields': ('financial_performance', 'compliance_performance')
        }),
        ('Analysis', {
            'fields': ('key_factors', 'recommendations')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        })
    )
