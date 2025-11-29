from rest_framework import serializers
from .models import (
    LicensingPortalIntegration, PortalSMIData, InstitutionalProfile,
    Shareholder, Director, LicenseHistory
)
from apps.core.serializers import SMISerializer

class LicensingPortalIntegrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = LicensingPortalIntegration
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']

class PortalSMIDataSerializer(serializers.ModelSerializer):
    smi = SMISerializer(read_only=True)
    smi_id = serializers.UUIDField(write_only=True)
    
    class Meta:
        model = PortalSMIData
        fields = '__all__'
        read_only_fields = ['id', 'last_updated_from_portal', 'created_at', 'updated_at']

class InstitutionalProfileSerializer(serializers.ModelSerializer):
    smi = SMISerializer(read_only=True)
    smi_id = serializers.UUIDField(write_only=True)
    
    class Meta:
        model = InstitutionalProfile
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']

class ShareholderSerializer(serializers.ModelSerializer):
    smi = SMISerializer(read_only=True)
    smi_id = serializers.UUIDField(write_only=True)
    
    class Meta:
        model = Shareholder
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']

class DirectorSerializer(serializers.ModelSerializer):
    smi = SMISerializer(read_only=True)
    smi_id = serializers.UUIDField(write_only=True)
    
    class Meta:
        model = Director
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']

class LicenseHistorySerializer(serializers.ModelSerializer):
    smi = SMISerializer(read_only=True)
    smi_id = serializers.UUIDField(write_only=True)
    
    class Meta:
        model = LicenseHistory
        fields = '__all__'
        read_only_fields = ['id', 'created_at']

class SMIInstitutionalDataSerializer(serializers.Serializer):
    """Comprehensive SMI institutional data serializer"""
    smi = SMISerializer()
    institutional_profile = InstitutionalProfileSerializer()
    shareholders = ShareholderSerializer(many=True)
    directors = DirectorSerializer(many=True)
    license_history = LicenseHistorySerializer(many=True)
    portal_data = PortalSMIDataSerializer()

class LicensingPortalSyncSerializer(serializers.Serializer):
    """Serializer for licensing portal synchronization"""
    smi_id = serializers.UUIDField()
    sync_type = serializers.ChoiceField(choices=['FULL', 'INCREMENTAL', 'SELECTIVE'])
    force_sync = serializers.BooleanField(default=False)
    
    def validate_smi_id(self, value):
        from apps.core.models import SMI
        try:
            SMI.objects.get(id=value)
        except SMI.DoesNotExist:
            raise serializers.ValidationError("SMI with this ID does not exist")
        return value

class PortalDataUpdateSerializer(serializers.Serializer):
    """Serializer for updating portal data"""
    portal_id = serializers.CharField(max_length=100)
    portal_status = serializers.CharField(max_length=50, required=False)
    portal_capital_adequacy = serializers.DecimalField(max_digits=15, decimal_places=2, required=False)
    portal_licensing_fee = serializers.DecimalField(max_digits=15, decimal_places=2, required=False)
    portal_annual_revenue = serializers.DecimalField(max_digits=20, decimal_places=2, required=False)
    
    def validate(self, data):
        if not data.get('portal_id'):
            raise serializers.ValidationError("Portal ID is required")
        return data

