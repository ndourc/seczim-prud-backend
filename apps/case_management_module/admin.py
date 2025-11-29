from django.contrib import admin
from .models import Case, CaseNote, Investigation, AdHocInspection, CaseAttachment, CaseTimeline

@admin.register(Case)
class CaseAdmin(admin.ModelAdmin):
    list_display = ['case_number', 'title', 'case_type', 'smi', 'status', 'priority', 'assigned_to', 'opened_date']
    list_filter = ['case_type', 'status', 'priority', 'opened_date']
    search_fields = ['case_number', 'title', 'smi__company_name', 'assigned_to__username']
    readonly_fields = ['case_number', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Case Information', {
            'fields': ('case_number', 'case_type', 'title', 'description')
        }),
        ('Related Entities', {
            'fields': ('smi', 'complainant')
        }),
        ('Assignment and Status', {
            'fields': ('assigned_to', 'status', 'priority')
        }),
        ('Timeline', {
            'fields': ('opened_date', 'due_date', 'resolved_date')
        }),
        ('Progress Tracking', {
            'fields': ('progress_notes', 'attachments')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

@admin.register(CaseNote)
class CaseNoteAdmin(admin.ModelAdmin):
    list_display = ['case', 'author', 'created_at']
    list_filter = ['created_at']
    search_fields = ['case__case_number', 'author__username', 'note']
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('Note Information', {
            'fields': ('case', 'author', 'note')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        })
    )

@admin.register(Investigation)
class InvestigationAdmin(admin.ModelAdmin):
    list_display = ['case', 'investigation_type', 'start_date', 'estimated_completion']
    list_filter = ['investigation_type', 'start_date']
    search_fields = ['case__case_number', 'scope', 'methodology']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Investigation Details', {
            'fields': ('case', 'investigation_type', 'scope', 'methodology')
        }),
        ('Findings', {
            'fields': ('evidence_collected', 'preliminary_findings', 'final_findings', 'recommendations')
        }),
        ('Timeline', {
            'fields': ('start_date', 'estimated_completion', 'actual_completion')
        }),
        ('Resources', {
            'fields': ('team_members', 'budget')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

@admin.register(AdHocInspection)
class AdHocInspectionAdmin(admin.ModelAdmin):
    list_display = ['case', 'trigger_type', 'inspection_scope', 'follow_up_required', 'estimated_duration']
    list_filter = ['trigger_type', 'follow_up_required', 'created_at']
    search_fields = ['case__case_number', 'inspection_scope', 'areas_of_focus']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Inspection Information', {
            'fields': ('case', 'trigger_type', 'inspection_scope', 'areas_of_focus', 'inspection_methodology')
        }),
        ('Findings and Actions', {
            'fields': ('immediate_findings', 'immediate_actions_required', 'follow_up_required', 'follow_up_date')
        }),
        ('Resources', {
            'fields': ('inspectors', 'estimated_duration')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

@admin.register(CaseAttachment)
class CaseAttachmentAdmin(admin.ModelAdmin):
    list_display = ['case', 'file_name', 'file_type', 'uploaded_by', 'uploaded_at']
    list_filter = ['file_type', 'uploaded_at']
    search_fields = ['file_name', 'case__case_number', 'uploaded_by__username']
    readonly_fields = ['uploaded_at']
    
    fieldsets = (
        ('File Information', {
            'fields': ('case', 'file', 'file_name', 'file_type', 'description')
        }),
        ('Upload Information', {
            'fields': ('uploaded_by', 'uploaded_at')
        })
    )

@admin.register(CaseTimeline)
class CaseTimelineAdmin(admin.ModelAdmin):
    list_display = ['case', 'event_type', 'event_date', 'user']
    list_filter = ['event_type', 'event_date']
    search_fields = ['case__case_number', 'event_type', 'description']
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('Event Information', {
            'fields': ('case', 'event_type', 'event_date', 'description', 'user')
        }),
        ('Additional Details', {
            'fields': ('notes', 'related_documents')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        })
    )
