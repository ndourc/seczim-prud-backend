from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from apps.core.models import SMI
import uuid

class Case(models.Model):
    """Case management for investigations and ad-hoc inspections"""
    CASE_TYPES = [
        ('INVESTIGATION', 'Investigation'),
        ('AD_HOC_INSPECTION', 'Ad-hoc Inspection'),
        ('COMPLAINT', 'Complaint Investigation'),
        ('REGULATORY_ACTION', 'Regulatory Action'),
        ('RISK_ESCALATION', 'Risk Escalation')
    ]
    
    STATUS_CHOICES = [
        ('OPEN', 'Open'),
        ('ASSIGNED', 'Assigned'),
        ('IN_PROGRESS', 'In Progress'),
        ('UNDER_REVIEW', 'Under Review'),
        ('RESOLVED', 'Resolved'),
        ('CLOSED', 'Closed')
    ]
    
    PRIORITY_CHOICES = [
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High'),
        ('URGENT', 'Urgent')
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    case_number = models.CharField(max_length=50, unique=True)
    case_type = models.CharField(max_length=30, choices=CASE_TYPES, default='INVESTIGATION')
    title = models.CharField(max_length=255, default='Case title to be provided')
    description = models.TextField(default='Case description to be provided')
    
    # Related Entities
    smi = models.ForeignKey(SMI, on_delete=models.CASCADE, related_name='cases', null=True, blank=True)
    complainant = models.CharField(max_length=255, blank=True)
    
    # Assignment and Status
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='OPEN')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='MEDIUM')
    
    # Timeline
    opened_date = models.DateField(default=timezone.localdate)
    due_date = models.DateField(null=True, blank=True)
    resolved_date = models.DateField(null=True, blank=True)
    
    # Progress Tracking
    progress_notes = models.TextField(blank=True)
    attachments = models.FileField(upload_to='case_attachments/', null=True, blank=True)
    
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.case_number} - {self.title}"

    def save(self, *args, **kwargs):
        if not self.case_number:
            self.case_number = f"CASE-{timezone.now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-opened_date']

class CaseNote(models.Model):
    """Progress notes and updates for cases"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='case_notes')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    note = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Note by {self.author.username} on {self.case.case_number}"

    class Meta:
        ordering = ['-created_at']

class Investigation(models.Model):
    """Detailed investigation information"""
    INVESTIGATION_TYPES = [
        ('REGULATORY', 'Regulatory Investigation'),
        ('COMPLIANCE', 'Compliance Investigation'),
        ('FINANCIAL', 'Financial Investigation'),
        ('OPERATIONAL', 'Operational Investigation'),
        ('FRAUD', 'Fraud Investigation')
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    case = models.OneToOneField(Case, on_delete=models.CASCADE, related_name='investigation')
    investigation_type = models.CharField(max_length=30, choices=INVESTIGATION_TYPES, default='REGULATORY')
    
    # Investigation Details
    scope = models.TextField(default='Investigation scope to be defined')
    methodology = models.TextField(default='Investigation methodology to be documented')
    evidence_collected = models.TextField(blank=True)
    
    # Findings
    preliminary_findings = models.TextField(blank=True)
    final_findings = models.TextField(blank=True)
    recommendations = models.TextField(blank=True)
    
    # Timeline
    start_date = models.DateField(default=timezone.localdate)
    estimated_completion = models.DateField(null=True, blank=True)
    actual_completion = models.DateField(null=True, blank=True)
    
    # Resources
    team_members = models.ManyToManyField(User, related_name='investigations', blank=True)
    budget = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Investigation - {self.case.case_number}"

class AdHocInspection(models.Model):
    """Ad-hoc inspection triggered by complaints or risk alerts"""
    INSPECTION_TRIGGERS = [
        ('COMPLAINT', 'Complaint Received'),
        ('RISK_ALERT', 'Risk Alert Triggered'),
        ('REGULATORY_REQUEST', 'Regulatory Request'),
        ('INTERNAL_ESCALATION', 'Internal Escalation'),
        ('MARKET_INTELLIGENCE', 'Market Intelligence')
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    case = models.OneToOneField(Case, on_delete=models.CASCADE, related_name='ad_hoc_inspection')
    trigger_type = models.CharField(max_length=30, choices=INSPECTION_TRIGGERS, default='COMPLAINT')
    
    # Inspection Details
    inspection_scope = models.TextField(default='Inspection scope to be defined')
    areas_of_focus = models.TextField(help_text="Specific areas to focus on: CDD, record-keeping, reporting compliance")
    inspection_methodology = models.TextField(default='Inspection methodology to be documented')
    
    # Findings and Actions
    immediate_findings = models.TextField(blank=True)
    immediate_actions_required = models.TextField(blank=True)
    follow_up_required = models.BooleanField(default=False)
    follow_up_date = models.DateField(null=True, blank=True)
    
    # Resources
    inspectors = models.ManyToManyField(User, related_name='ad_hoc_inspections', blank=True)
    estimated_duration = models.IntegerField(help_text="Estimated duration in days", default=1)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Ad-hoc Inspection - {self.case.case_number}"

class CaseAttachment(models.Model):
    """File attachments for cases"""
    ATTACHMENT_TYPES = [
        ('DOCUMENT', 'Document'),
        ('IMAGE', 'Image'),
        ('AUDIO', 'Audio'),
        ('VIDEO', 'Video'),
        ('OTHER', 'Other')
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='case_attachments')
    file = models.FileField(upload_to='case_attachments/')
    file_name = models.CharField(max_length=255)
    file_type = models.CharField(max_length=20, choices=ATTACHMENT_TYPES, default='DOCUMENT')
    description = models.TextField(blank=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.file_name} - {self.case.case_number}"

    class Meta:
        ordering = ['-uploaded_at']

class CaseTimeline(models.Model):
    """Timeline events for case tracking"""
    EVENT_TYPES = [
        ('CASE_OPENED', 'Case Opened'),
        ('ASSIGNED', 'Case Assigned'),
        ('INVESTIGATION_STARTED', 'Investigation Started'),
        ('INSPECTION_SCHEDULED', 'Inspection Scheduled'),
        ('INSPECTION_COMPLETED', 'Inspection Completed'),
        ('FINDINGS_REPORTED', 'Findings Reported'),
        ('ACTIONS_TAKEN', 'Actions Taken'),
        ('CASE_RESOLVED', 'Case Resolved'),
        ('CASE_CLOSED', 'Case Closed')
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='timeline_events')
    event_type = models.CharField(max_length=30, choices=EVENT_TYPES, default='CASE_OPENED')
    event_date = models.DateTimeField(default=timezone.now)
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Additional Details
    notes = models.TextField(blank=True)
    related_documents = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.event_type} - {self.case.case_number} - {self.event_date}"

    class Meta:
        ordering = ['event_date']
