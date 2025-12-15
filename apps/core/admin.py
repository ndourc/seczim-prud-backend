from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import (
    SMI, BoardMember, MeetingLog, ProductOffering, ClienteleProfile,
    FinancialStatement, ClientAssetMix, LicensingBreach, SupervisoryIntervention,
    Notification, SystemAuditLog
)
from .formula_models import CalculationFormula, CalculationBreakdown

@admin.register(SMI)
class SMIAdmin(admin.ModelAdmin):
    list_display = ['company_name', 'license_number', 'status', 'registration_date', 'business_type', 'created_at']
    list_filter = ['status', 'business_type', 'registration_date', 'created_at']
    search_fields = ['company_name', 'license_number', 'email', 'phone']
    readonly_fields = ['id', 'created_at', 'updated_at']
    ordering = ['company_name']
    list_per_page = 25
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('company_name', 'license_number', 'registration_date', 'business_type')
        }),
        ('Contact Information', {
            'fields': ('address', 'phone', 'email', 'website')
        }),
        ('Status & Metadata', {
            'fields': ('status', 'id', 'created_at', 'updated_at')
        }),
    )

@admin.register(BoardMember)
class BoardMemberAdmin(admin.ModelAdmin):
    list_display = ['name', 'position', 'smi', 'appointment_date', 'is_active']
    list_filter = ['position', 'is_active', 'appointment_date', 'smi__status']
    search_fields = ['name', 'position', 'smi__company_name']
    list_per_page = 25

@admin.register(MeetingLog)
class MeetingLogAdmin(admin.ModelAdmin):
    list_display = ['meeting_type', 'smi', 'meeting_date', 'created_at']
    list_filter = ['meeting_type', 'meeting_date', 'smi__status']
    search_fields = ['smi__company_name', 'agenda', 'decisions']
    list_per_page = 25

@admin.register(ProductOffering)
class ProductOfferingAdmin(admin.ModelAdmin):
    list_display = ['product_name', 'smi', 'product_category', 'income_contribution', 'is_active']
    list_filter = ['product_category', 'is_active', 'smi__status']
    search_fields = ['product_name', 'smi__company_name']
    list_per_page = 25

@admin.register(ClienteleProfile)
class ClienteleProfileAdmin(admin.ModelAdmin):
    list_display = ['client_type', 'smi', 'client_count', 'income_contribution', 'period']
    list_filter = ['client_type', 'period', 'smi__status']
    search_fields = ['smi__company_name']
    list_per_page = 25

@admin.register(FinancialStatement)
class FinancialStatementAdmin(admin.ModelAdmin):
    list_display = ['smi', 'period', 'statement_type', 'total_revenue', 'total_assets', 'created_at']
    list_filter = ['statement_type', 'period', 'smi__status']
    search_fields = ['smi__company_name']
    readonly_fields = ['created_at', 'updated_at']
    list_per_page = 25

@admin.register(ClientAssetMix)
class ClientAssetMixAdmin(admin.ModelAdmin):
    list_display = ['smi', 'period', 'asset_class', 'allocation_percentage', 'sec_compliance_status']
    list_filter = ['asset_class', 'sec_compliance_status', 'period', 'smi__status']
    search_fields = ['smi__company_name']
    list_per_page = 25



@admin.register(LicensingBreach)
class LicensingBreachAdmin(admin.ModelAdmin):
    list_display = ['breach_type', 'smi', 'breach_date', 'status', 'assigned_to', 'penalty_amount']
    list_filter = ['breach_type', 'status', 'breach_date', 'smi__status']
    search_fields = ['smi__company_name', 'assigned_to__username', 'description']
    readonly_fields = ['created_at', 'updated_at']
    list_per_page = 25

@admin.register(SupervisoryIntervention)
class SupervisoryInterventionAdmin(admin.ModelAdmin):
    list_display = ['intervention_type', 'smi', 'intervention_date', 'intensity', 'frequency', 'follow_up_required']
    list_filter = ['intervention_type', 'intensity', 'frequency', 'follow_up_required', 'intervention_date']
    search_fields = ['smi__company_name', 'reason', 'description']
    list_per_page = 25



@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['notification_type', 'user', 'title', 'priority', 'read', 'email_sent', 'created_at']
    list_filter = ['notification_type', 'priority', 'read', 'email_sent', 'created_at']
    search_fields = ['user__username', 'title', 'message']
    readonly_fields = ['created_at', 'read_at', 'email_sent_at']
    list_per_page = 25

@admin.register(SystemAuditLog)
class SystemAuditLogAdmin(admin.ModelAdmin):
    list_display = ['action', 'user', 'model_name', 'object_repr', 'timestamp', 'ip_address']
    list_filter = ['action', 'model_name', 'timestamp']
    search_fields = ['user__username', 'action', 'model_name', 'object_repr']
    readonly_fields = ['timestamp']
    list_per_page = 25

@admin.register(CalculationFormula)
class CalculationFormulaAdmin(admin.ModelAdmin):
    list_display = ['formula_type', 'name', 'version', 'is_active', 'updated_by', 'updated_at']
    list_filter = ['formula_type', 'is_active', 'created_at', 'updated_at']
    search_fields = ['name', 'description', 'formula_type']
    readonly_fields = ['id', 'created_at', 'updated_at', 'version']
    list_per_page = 25
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('formula_type', 'name', 'description', 'is_active')
        }),
        ('Formula Definition', {
            'fields': ('formula_expression', 'variables', 'weights', 'thresholds')
        }),
        ('Metadata', {
            'fields': ('version', 'created_by', 'updated_by', 'change_notes', 'id', 'created_at', 'updated_at')
        }),
    )

@admin.register(CalculationBreakdown)
class CalculationBreakdownAdmin(admin.ModelAdmin):
    list_display = ['calculation_type', 'reference_id', 'final_value', 'final_percentage', 'calculated_at']
    list_filter = ['calculation_type', 'calculated_at']
    search_fields = ['calculation_type', 'reference_id', 'calculated_by']
    readonly_fields = ['id', 'calculated_at']
    list_per_page = 25
    
    fieldsets = (
        ('Calculation Info', {
            'fields': ('calculation_type', 'reference_id', 'formula')
        }),
        ('Results', {
            'fields': ('final_value', 'final_percentage', 'components')
        }),
        ('Metadata', {
            'fields': ('calculated_at', 'calculated_by', 'id')
        }),
    )
