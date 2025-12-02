from rest_framework import serializers
from .models import Case, CaseNote, Investigation, AdHocInspection, CaseAttachment, CaseTimeline
from apps.core.serializers import SMISerializer
from apps.core.models import SMI

class CaseSerializer(serializers.ModelSerializer):
    smi = SMISerializer(read_only=True)
    smi_id = serializers.PrimaryKeyRelatedField(
        queryset=SMI.objects.all(), source='smi', write_only=True, required=False, allow_null=True
    )
    assigned_to = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = Case
        fields = '__all__'
        read_only_fields = ['id', 'case_number', 'created_at', 'updated_at']

class CaseNoteSerializer(serializers.ModelSerializer):
    case = serializers.PrimaryKeyRelatedField(queryset=Case.objects.all())
    author = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = CaseNote
        fields = '__all__'
        read_only_fields = ['id', 'created_at']

class InvestigationSerializer(serializers.ModelSerializer):
    case = serializers.PrimaryKeyRelatedField(queryset=Case.objects.all())
    team_members = serializers.StringRelatedField(many=True, read_only=True)
    
    class Meta:
        model = Investigation
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']

class AdHocInspectionSerializer(serializers.ModelSerializer):
    case = serializers.PrimaryKeyRelatedField(queryset=Case.objects.all())
    inspectors = serializers.StringRelatedField(many=True, read_only=True)
    
    class Meta:
        model = AdHocInspection
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']

class CaseAttachmentSerializer(serializers.ModelSerializer):
    case = serializers.PrimaryKeyRelatedField(queryset=Case.objects.all())
    uploaded_by = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = CaseAttachment
        fields = '__all__'
        read_only_fields = ['id', 'uploaded_at']

class CaseTimelineSerializer(serializers.ModelSerializer):
    case = serializers.PrimaryKeyRelatedField(queryset=Case.objects.all())
    user = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = CaseTimeline
        fields = '__all__'
        read_only_fields = ['id', 'created_at']

class CaseSummarySerializer(serializers.Serializer):
    """Summary serializer for case dashboard"""
    case = CaseSerializer()
    investigation = InvestigationSerializer()
    ad_hoc_inspection = AdHocInspectionSerializer()
    recent_notes = CaseNoteSerializer(many=True)
    timeline_events = CaseTimelineSerializer(many=True)
    attachments_count = serializers.IntegerField()

class CaseDashboardSerializer(serializers.Serializer):
    """Dashboard serializer for case management"""
    total_cases = serializers.IntegerField()
    open_cases = serializers.IntegerField()
    in_progress_cases = serializers.IntegerField()
    resolved_cases = serializers.IntegerField()
    urgent_cases = serializers.IntegerField()
    recent_cases = CaseSerializer(many=True)

