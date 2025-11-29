from rest_framework import serializers
from .models import RiskAssessment, StressTest, RiskIndicator, RiskTrend
from apps.core.serializers import SMISerializer

class RiskAssessmentSerializer(serializers.ModelSerializer):
    smi = SMISerializer(read_only=True)
    smi_id = serializers.UUIDField(write_only=True)
    
    class Meta:
        model = RiskAssessment
        fields = '__all__'
        read_only_fields = ['id', 'overall_risk_score', 'risk_level', 'created_at', 'updated_at']

class StressTestSerializer(serializers.ModelSerializer):
    smi = SMISerializer(read_only=True)
    smi_id = serializers.UUIDField(write_only=True, required=False)
    
    class Meta:
        model = StressTest
        fields = '__all__'
        read_only_fields = ['id', 'created_at']

class RiskIndicatorSerializer(serializers.ModelSerializer):
    smi = SMISerializer(read_only=True)
    smi_id = serializers.UUIDField(write_only=True)
    
    class Meta:
        model = RiskIndicator
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']

class RiskTrendSerializer(serializers.ModelSerializer):
    smi = SMISerializer(read_only=True)
    smi_id = serializers.UUIDField(write_only=True)
    
    class Meta:
        model = RiskTrend
        fields = '__all__'
        read_only_fields = ['id', 'created_at']

class RiskAssessmentSummarySerializer(serializers.Serializer):
    """Summary serializer for risk assessment dashboard"""
    smi = SMISerializer()
    latest_assessment = RiskAssessmentSerializer()
    risk_trend = serializers.CharField()
    alert_level = serializers.CharField()
    next_assessment_date = serializers.DateField()

class StressTestSummarySerializer(serializers.Serializer):
    """Summary serializer for stress testing dashboard"""
    smi = SMISerializer()
    total_tests = serializers.IntegerField()
    passed_tests = serializers.IntegerField()
    failed_tests = serializers.IntegerField()
    last_test_date = serializers.DateField()
    next_test_date = serializers.DateField()

class RiskIndicatorAlertSerializer(serializers.Serializer):
    """Serializer for risk indicator alerts"""
    indicator_name = serializers.CharField()
    current_value = serializers.FloatField()
    threshold_value = serializers.FloatField()
    breach_level = serializers.CharField()
    smi_name = serializers.CharField()
    alert_message = serializers.CharField()

