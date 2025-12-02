from rest_framework import serializers
from .models import ComplianceIndex, ComplianceAssessment, ComplianceRequirement, ComplianceViolation, ComplianceReport
from apps.core.serializers import SMISerializer
from apps.core.models import SMI

class ComplianceIndexSerializer(serializers.ModelSerializer):
    smi = SMISerializer(read_only=True)
    smi_id = serializers.PrimaryKeyRelatedField(
        queryset=SMI.objects.all(), source='smi', write_only=True
    )
    
    class Meta:
        model = ComplianceIndex
        fields = '__all__'
        read_only_fields = ['id', 'final_compliance_score', 'created_at', 'updated_at']

class ComplianceAssessmentSerializer(serializers.ModelSerializer):
    smi = SMISerializer(read_only=True)
    smi_id = serializers.PrimaryKeyRelatedField(
        queryset=SMI.objects.all(), source='smi', write_only=True
    )
    
    class Meta:
        model = ComplianceAssessment
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']

class ComplianceRequirementSerializer(serializers.ModelSerializer):
    smi = SMISerializer(read_only=True)
    smi_id = serializers.PrimaryKeyRelatedField(
        queryset=SMI.objects.all(), source='smi', write_only=True
    )
    
    class Meta:
        model = ComplianceRequirement
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']

class ComplianceViolationSerializer(serializers.ModelSerializer):
    smi = SMISerializer(read_only=True)
    smi_id = serializers.PrimaryKeyRelatedField(
        queryset=SMI.objects.all(), source='smi', write_only=True
    )
    compliance_requirement = serializers.PrimaryKeyRelatedField(queryset=ComplianceRequirement.objects.all())
    
    class Meta:
        model = ComplianceViolation
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']

class ComplianceReportSerializer(serializers.ModelSerializer):
    smi = SMISerializer(read_only=True)
    smi_id = serializers.PrimaryKeyRelatedField(
        queryset=SMI.objects.all(), source='smi', write_only=True
    )
    prepared_by = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = ComplianceReport
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']

class ComplianceDashboardSerializer(serializers.Serializer):
    """Dashboard serializer for compliance management"""
    total_smis = serializers.IntegerField()
    compliant_smis = serializers.IntegerField()
    non_compliant_smis = serializers.IntegerField()
    pending_assessments = serializers.IntegerField()
    recent_violations = serializers.IntegerField()
    average_compliance_score = serializers.FloatField()
    recent_reports = ComplianceReportSerializer(many=True)

class ComplianceSummarySerializer(serializers.Serializer):
    """Summary serializer for compliance overview"""
    smi = SMISerializer()
    latest_compliance_index = ComplianceIndexSerializer()
    latest_assessment = ComplianceAssessmentSerializer()
    active_requirements = ComplianceRequirementSerializer(many=True)
    recent_violations = ComplianceViolationSerializer(many=True)
    compliance_trend = serializers.CharField()
