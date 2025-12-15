from rest_framework import serializers
from .formula_models import CalculationFormula, CalculationBreakdown


class CalculationFormulaSerializer(serializers.ModelSerializer):
    """Serializer for calculation formulae"""
    created_by_name = serializers.CharField(source='created_by.username', read_only=True)
    updated_by_name = serializers.CharField(source='updated_by.username', read_only=True)
    formula_type_display = serializers.CharField(source='get_formula_type_display', read_only=True)
    
    class Meta:
        model = CalculationFormula
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at', 'version']
    
    def create(self, validated_data):
        # Set the user who created the formula
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['created_by'] = request.user
            validated_data['updated_by'] = request.user
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        # Increment version and set updated_by
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['updated_by'] = request.user
        
        # Increment version on update
        instance.version += 1
        return super().update(instance, validated_data)


class CalculationBreakdownSerializer(serializers.ModelSerializer):
    """Serializer for calculation breakdowns"""
    formula_name = serializers.CharField(source='formula.name', read_only=True)
    formula_type = serializers.CharField(source='formula.formula_type', read_only=True)
    
    class Meta:
        model = CalculationBreakdown
        fields = '__all__'
        read_only_fields = ['id', 'calculated_at']


class CalculationBreakdownDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer for calculation breakdowns with full formula info"""
    formula = CalculationFormulaSerializer(read_only=True)
    
    class Meta:
        model = CalculationBreakdown
        fields = '__all__'
        read_only_fields = ['id', 'calculated_at']
