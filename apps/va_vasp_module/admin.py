from django.contrib import admin
from .models import VA_VASP, VirtualAsset, VASPService, VARiskAssessment, VASPCompliance

@admin.register(VA_VASP)
class VA_VASPAdmin(admin.ModelAdmin):
    list_display = ['smi', 'analysis_date', 'is_va_issuer', 'is_vasp', 'overall_va_risk_score', 'securities_exposure']
    list_filter = ['is_va_issuer', 'is_vasp', 'analysis_date']
    search_fields = ['smi__company_name', 'va_types', 'risk_profile']
    readonly_fields = ['overall_va_risk_score', 'created_at', 'updated_at']
    
    fieldsets = (
        ('SMI Information', {
            'fields': ('smi', 'analysis_date')
        }),
        ('VA/VASP Classification', {
            'fields': ('is_va_issuer', 'is_vasp', 'va_types')
        }),
        ('Risk Assessment', {
            'fields': ('va_risk_score', 'vasp_risk_score', 'overall_va_risk_score')
        }),
        ('Securities Sector', {
            'fields': ('securities_exposure', 'regulatory_compliance')
        }),
        ('Risk Profile Outputs', {
            'fields': ('risk_profile', 'recommendations')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

@admin.register(VirtualAsset)
class VirtualAssetAdmin(admin.ModelAdmin):
    list_display = ['asset_name', 'asset_symbol', 'asset_category', 'va_vasp_analysis', 'risk_level', 'risk_score']
    list_filter = ['asset_category', 'risk_level', 'regulatory_status', 'created_at']
    search_fields = ['asset_name', 'asset_symbol', 'va_vasp_analysis__smi__company_name']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Asset Information', {
            'fields': ('va_vasp_analysis', 'asset_name', 'asset_symbol', 'asset_category')
        }),
        ('Asset Characteristics', {
            'fields': ('market_cap', 'trading_volume', 'volatility_index')
        }),
        ('Risk Assessment', {
            'fields': ('risk_level', 'risk_score', 'risk_factors')
        }),
        ('Regulatory Status', {
            'fields': ('regulatory_status', 'compliance_requirements')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

@admin.register(VASPService)
class VASPServiceAdmin(admin.ModelAdmin):
    list_display = ['service_name', 'service_type', 'va_vasp_analysis', 'is_active', 'customer_count', 'service_risk_score']
    list_filter = ['service_type', 'is_active', 'compliance_status', 'created_at']
    search_fields = ['service_name', 'va_vasp_analysis__smi__company_name']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Service Information', {
            'fields': ('va_vasp_analysis', 'service_type', 'service_name', 'service_description')
        }),
        ('Service Characteristics', {
            'fields': ('is_active', 'customer_count', 'transaction_volume')
        }),
        ('Risk Assessment', {
            'fields': ('service_risk_score', 'risk_mitigation_measures')
        }),
        ('Compliance', {
            'fields': ('regulatory_licenses', 'compliance_status')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

@admin.register(VARiskAssessment)
class VARiskAssessmentAdmin(admin.ModelAdmin):
    list_display = ['va_vasp_analysis', 'risk_category', 'risk_score', 'risk_probability', 'risk_impact', 'assessment_date']
    list_filter = ['risk_category', 'risk_probability', 'risk_impact', 'assessment_date']
    search_fields = ['risk_category', 'va_vasp_analysis__smi__company_name', 'risk_description']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Assessment Information', {
            'fields': ('va_vasp_analysis', 'risk_category', 'assessment_date')
        }),
        ('Risk Metrics', {
            'fields': ('risk_score', 'risk_probability', 'risk_impact')
        }),
        ('Risk Details', {
            'fields': ('risk_description', 'risk_factors', 'mitigation_strategies')
        }),
        ('Assessment', {
            'fields': ('assessor_notes',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

@admin.register(VASPCompliance)
class VASPComplianceAdmin(admin.ModelAdmin):
    list_display = ['va_vasp_analysis', 'compliance_area', 'compliance_status', 'compliance_score', 'assessment_date']
    list_filter = ['compliance_area', 'compliance_status', 'follow_up_required', 'assessment_date']
    search_fields = ['compliance_area', 'va_vasp_analysis__smi__company_name', 'requirements']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Compliance Information', {
            'fields': ('va_vasp_analysis', 'compliance_area', 'compliance_status', 'compliance_score')
        }),
        ('Requirements and Assessment', {
            'fields': ('requirements', 'current_status', 'gaps_identified', 'remediation_plan')
        }),
        ('Timeline', {
            'fields': ('assessment_date', 'target_compliance_date', 'actual_compliance_date')
        }),
        ('Follow-up', {
            'fields': ('follow_up_required', 'follow_up_date', 'follow_up_notes')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
