from rest_framework import serializers
from .models import PrudentialReturn, IncomeStatement, BalanceSheet
from apps.core.serializers import SMISerializer
from apps.core.models import SMI

class PrudentialReturnSerializer(serializers.ModelSerializer):
    smi = SMISerializer(read_only=True)
    smi_id = serializers.PrimaryKeyRelatedField(
        queryset=SMI.objects.all(), source='smi', write_only=True
    )
    
    class Meta:
        model = PrudentialReturn
        fields = '__all__'
        read_only_fields = ['id', 'case_number', 'created_at', 'updated_at']

class IncomeStatementSerializer(serializers.ModelSerializer):
    prudential_return = serializers.PrimaryKeyRelatedField(queryset=PrudentialReturn.objects.all())
    
    class Meta:
        model = IncomeStatement
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']

class BalanceSheetSerializer(serializers.ModelSerializer):
    prudential_return = serializers.PrimaryKeyRelatedField(queryset=PrudentialReturn.objects.all())
    
    class Meta:
        model = BalanceSheet
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']

class PrudentialReturnSummarySerializer(serializers.Serializer):
    """Summary serializer for prudential returns"""
    prudential_return = PrudentialReturnSerializer()
    income_statement = IncomeStatementSerializer()
    balance_sheet = BalanceSheetSerializer()

class ReturnsDashboardSerializer(serializers.Serializer):
    """Dashboard serializer for returns management"""
    total_returns = serializers.IntegerField()
    submitted_returns = serializers.IntegerField()
    pending_returns = serializers.IntegerField()
    approved_returns = serializers.IntegerField()
    rejected_returns = serializers.IntegerField()
    recent_returns = PrudentialReturnSerializer(many=True)
