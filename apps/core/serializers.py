from rest_framework import serializers
from .models import (
    SMI, BoardMember, MeetingLog, ProductOffering, ClienteleProfile,
    FinancialStatement, ClientAssetMix, LicensingBreach, SupervisoryIntervention,
    Notification, SystemAuditLog
)

class SMISerializer(serializers.ModelSerializer):
    class Meta:
        model = SMI
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']

class BoardMemberSerializer(serializers.ModelSerializer):
    smi = SMISerializer(read_only=True)
    smi_id = serializers.UUIDField(write_only=True)
    
    class Meta:
        model = BoardMember
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']

class MeetingLogSerializer(serializers.ModelSerializer):
    smi = SMISerializer(read_only=True)
    smi_id = serializers.UUIDField(write_only=True)
    
    class Meta:
        model = MeetingLog
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']

class ProductOfferingSerializer(serializers.ModelSerializer):
    smi = SMISerializer(read_only=True)
    smi_id = serializers.UUIDField(write_only=True)
    
    class Meta:
        model = ProductOffering
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']

class ClienteleProfileSerializer(serializers.ModelSerializer):
    smi = SMISerializer(read_only=True)
    smi_id = serializers.UUIDField(write_only=True)
    
    class Meta:
        model = ClienteleProfile
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']

class FinancialStatementSerializer(serializers.ModelSerializer):
    smi = SMISerializer(read_only=True)
    smi_id = serializers.UUIDField(write_only=True)
    
    class Meta:
        model = FinancialStatement
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']

class ClientAssetMixSerializer(serializers.ModelSerializer):
    smi = SMISerializer(read_only=True)
    smi_id = serializers.UUIDField(write_only=True)
    
    class Meta:
        model = ClientAssetMix
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']



class LicensingBreachSerializer(serializers.ModelSerializer):
    smi = SMISerializer(read_only=True)
    smi_id = serializers.UUIDField(write_only=True)
    assigned_to = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = LicensingBreach
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']

class SupervisoryInterventionSerializer(serializers.ModelSerializer):
    smi = SMISerializer(read_only=True)
    smi_id = serializers.UUIDField(write_only=True)
    
    class Meta:
        model = SupervisoryIntervention
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']



class NotificationSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = Notification
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']

class SystemAuditLogSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    ip_address = serializers.CharField(max_length=45)
    
    class Meta:
        model = SystemAuditLog
        fields = '__all__'
        read_only_fields = ['id', 'created_at']

class SMIDashboardSerializer(serializers.Serializer):
    """Dashboard serializer for SMI management"""
    total_smis = serializers.IntegerField()
    active_smis = serializers.IntegerField()
    suspended_smis = serializers.IntegerField()
    revoked_smis = serializers.IntegerField()
    recent_smis = SMISerializer(many=True)
    high_risk_smis = serializers.IntegerField()
    compliance_alerts = serializers.IntegerField()

class SMISummarySerializer(serializers.Serializer):
    """Summary serializer for SMI overview"""
    smi = SMISerializer()
    board_members = BoardMemberSerializer(many=True)
    recent_meetings = MeetingLogSerializer(many=True)
    product_offerings = ProductOfferingSerializer(many=True)
    clientele_profiles = ClienteleProfileSerializer(many=True)
    latest_financial_statement = FinancialStatementSerializer()

class SMIDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer for SMI with related data"""
    board_members = BoardMemberSerializer(many=True, read_only=True)
    meeting_logs = MeetingLogSerializer(many=True, read_only=True)
    product_offerings = ProductOfferingSerializer(many=True, read_only=True)
    clientele_profiles = ClienteleProfileSerializer(many=True, read_only=True)
    financial_statements = FinancialStatementSerializer(many=True, read_only=True)
    client_asset_mixes = ClientAssetMixSerializer(many=True, read_only=True)
    licensing_breaches = LicensingBreachSerializer(many=True, read_only=True)
    supervisory_interventions = SupervisoryInterventionSerializer(many=True, read_only=True)
    
    class Meta:
        model = SMI
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']