from rest_framework import serializers
from .models import VA_VASP, VirtualAsset, VASPService, VARiskAssessment, VASPCompliance
from apps.core.serializers import SMISerializer
from apps.core.models import SMI

class VA_VASPSerializer(serializers.ModelSerializer):
    smi = SMISerializer(read_only=True)
    smi_id = serializers.PrimaryKeyRelatedField(
        queryset=SMI.objects.all(), source='smi', write_only=True
    )
    
    class Meta:
        model = VA_VASP
        fields = '__all__'
        read_only_fields = ['id', 'overall_va_risk_score', 'created_at', 'updated_at']

class VirtualAssetSerializer(serializers.ModelSerializer):
    va_vasp_analysis = serializers.PrimaryKeyRelatedField(queryset=VA_VASP.objects.all())
    
    class Meta:
        model = VirtualAsset
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']

class VASPServiceSerializer(serializers.ModelSerializer):
    va_vasp_analysis = serializers.PrimaryKeyRelatedField(queryset=VA_VASP.objects.all())
    
    class Meta:
        model = VASPService
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']

class VARiskAssessmentSerializer(serializers.ModelSerializer):
    va_vasp_analysis = serializers.PrimaryKeyRelatedField(queryset=VA_VASP.objects.all())
    
    class Meta:
        model = VARiskAssessment
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']

class VASPComplianceSerializer(serializers.ModelSerializer):
    va_vasp_analysis = serializers.PrimaryKeyRelatedField(queryset=VA_VASP.objects.all())
    
    class Meta:
        model = VASPCompliance
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']

class VA_VASPSummarySerializer(serializers.Serializer):
    """Summary serializer for VA/VASP dashboard"""
    va_vasp = VA_VASPSerializer()
    virtual_assets = VirtualAssetSerializer(many=True)
    vasp_services = VASPServiceSerializer(many=True)
    risk_assessments = VARiskAssessmentSerializer(many=True)
    compliance_status = VASPComplianceSerializer(many=True)

class VA_VASPDashboardSerializer(serializers.Serializer):
    """Dashboard serializer for VA/VASP management"""
    total_va_issuers = serializers.IntegerField()
    total_vasps = serializers.IntegerField()
    high_risk_entities = serializers.IntegerField()
    compliance_alerts = serializers.IntegerField()
    recent_analyses = VA_VASPSerializer(many=True)

