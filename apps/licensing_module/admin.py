from django.contrib import admin
from .models import (
    LicensingPortalIntegration, PortalSMIData, InstitutionalProfile,
    Shareholder, Director, LicenseHistory
)

@admin.register(LicensingPortalIntegration)
class LicensingPortalIntegrationAdmin(admin.ModelAdmin):
    list_display = ['portal_name', 'status', 'last_sync', 'sync_frequency', 'auto_sync_enabled']
    list_filter = ['status', 'sync_frequency', 'auto_sync_enabled']
    search_fields = ['portal_name', 'api_endpoint']
    readonly_fields = ['last_sync', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Portal Information', {
            'fields': ('portal_name', 'api_endpoint', 'api_key')
        }),
        ('Integration Status', {
            'fields': ('status', 'last_sync', 'sync_frequency')
        }),
        ('Configuration', {
            'fields': ('auto_sync_enabled', 'sync_errors')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

@admin.register(PortalSMIData)
class PortalSMIDataAdmin(admin.ModelAdmin):
    list_display = ['smi', 'portal_id', 'portal_status', 'sync_status', 'last_updated_from_portal']
    list_filter = ['portal_status', 'sync_status', 'portal_created_date']
    search_fields = ['smi__company_name', 'portal_id']
    readonly_fields = ['last_updated_from_portal', 'created_at', 'updated_at']
    
    fieldsets = (
        ('SMI Information', {
            'fields': ('smi', 'portal_id', 'portal_status')
        }),
        ('Financial Data', {
            'fields': ('portal_capital_adequacy', 'portal_licensing_fee', 'portal_annual_revenue')
        }),
        ('Portal Metadata', {
            'fields': ('portal_created_date', 'portal_last_review_date', 'portal_next_review_date')
        }),
        ('Sync Information', {
            'fields': ('sync_status', 'last_updated_from_portal')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

@admin.register(InstitutionalProfile)
class InstitutionalProfileAdmin(admin.ModelAdmin):
    list_display = ['smi', 'competitive_position', 'financial_strength', 'risk_appetite', 'number_of_employees']
    list_filter = ['competitive_position', 'financial_strength', 'risk_appetite']
    search_fields = ['smi__company_name', 'business_model']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Business Profile', {
            'fields': ('smi', 'business_model', 'target_markets', 'competitive_position')
        }),
        ('Financial Profile', {
            'fields': ('credit_rating', 'debt_rating', 'financial_strength')
        }),
        ('Risk Profile', {
            'fields': ('risk_appetite',)
        }),
        ('Operational Profile', {
            'fields': ('number_of_employees', 'number_of_branches', 'operating_countries')
        }),
        ('Compliance Profile', {
            'fields': ('compliance_history', 'regulatory_relationships')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

@admin.register(Shareholder)
class ShareholderAdmin(admin.ModelAdmin):
    list_display = ['name', 'smi', 'shareholder_type', 'ownership_percentage', 'is_active']
    list_filter = ['shareholder_type', 'is_active', 'regulatory_approval']
    search_fields = ['name', 'smi__company_name']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Shareholder Information', {
            'fields': ('name', 'shareholder_type', 'nationality')
        }),
        ('Ownership Details', {
            'fields': ('smi', 'ownership_percentage', 'shares_held', 'voting_rights')
        }),
        ('Financial Details', {
            'fields': ('investment_amount', 'investment_date')
        }),
        ('Regulatory Information', {
            'fields': ('regulatory_approval', 'approval_date', 'approval_reference')
        }),
        ('Status', {
            'fields': ('is_active', 'notes')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

@admin.register(Director)
class DirectorAdmin(admin.ModelAdmin):
    list_display = ['name', 'smi', 'director_type', 'is_active', 'fit_and_proper_assessment']
    list_filter = ['director_type', 'is_active', 'fit_and_proper_assessment', 'compliance_status']
    search_fields = ['name', 'smi__company_name']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Personal Details', {
            'fields': ('name', 'director_type', 'nationality', 'date_of_birth')
        }),
        ('Professional Details', {
            'fields': ('qualifications', 'experience_years', 'previous_positions')
        }),
        ('Appointment Details', {
            'fields': ('smi', 'appointment_date', 'resignation_date', 'is_active')
        }),
        ('Regulatory Information', {
            'fields': ('regulatory_approval', 'approval_date', 'fit_and_proper_assessment')
        }),
        ('Compliance', {
            'fields': ('training_completed', 'last_training_date', 'compliance_status')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

@admin.register(LicenseHistory)
class LicenseHistoryAdmin(admin.ModelAdmin):
    list_display = ['smi', 'change_type', 'change_date', 'license_number', 'is_active']
    list_filter = ['change_type', 'is_active', 'effective_date']
    search_fields = ['smi__company_name', 'license_number']
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('Change Information', {
            'fields': ('change_type', 'change_date', 'effective_date')
        }),
        ('License Details', {
            'fields': ('smi', 'license_number', 'license_type', 'license_scope', 'license_conditions')
        }),
        ('Regulatory Information', {
            'fields': ('regulatory_authority', 'approval_reference', 'regulatory_officer')
        }),
        ('Financial Information', {
            'fields': ('license_fee', 'security_deposit')
        }),
        ('Timeline', {
            'fields': ('expiry_date', 'renewal_due_date')
        }),
        ('Status', {
            'fields': ('is_active', 'notes')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        })
    )

