from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
import logging

from .formula_models import CalculationFormula, CalculationBreakdown
from .formula_serializers import (
    CalculationFormulaSerializer,
    CalculationBreakdownSerializer,
    CalculationBreakdownDetailSerializer
)

logger = logging.getLogger(__name__)


class CalculationFormulaViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing calculation formulae.
    Only admins can create, update, or delete formulae.
    """
    queryset = CalculationFormula.objects.all()
    serializer_class = CalculationFormulaSerializer
    permission_classes = [permissions.IsAdminUser]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'formula_type', 'description']
    ordering_fields = ['formula_type', 'version', 'updated_at']
    ordering = ['formula_type', '-version']
    
    def get_permissions(self):
        # Allow read-only access for authenticated users
        if self.action in ['list', 'retrieve']:
            return [permissions.IsAuthenticated()]
        # Only admins can modify formulae
        return [permissions.IsAdminUser()]
    
    @action(detail=False, methods=['get'])
    def by_type(self, request):
        """Get formula by type"""
        formula_type = request.query_params.get('type')
        if not formula_type:
            return Response(
                {'error': 'Formula type parameter is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            formula = self.queryset.filter(
                formula_type=formula_type,
                is_active=True
            ).first()
            
            if not formula:
                return Response(
                    {'error': f'No active formula found for type: {formula_type}'},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            serializer = self.get_serializer(formula)
            return Response(serializer.data)
        except Exception as e:
            logger.error(f"Error retrieving formula by type: {str(e)}")
            return Response(
                {'error': 'Failed to retrieve formula'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=True, methods=['post'])
    def activate(self, request, pk=None):
        """Activate a formula (deactivates others of the same type)"""
        formula = self.get_object()
        
        # Deactivate all other formulae of the same type
        CalculationFormula.objects.filter(
            formula_type=formula.formula_type
        ).exclude(id=formula.id).update(is_active=False)
        
        # Activate this formula
        formula.is_active = True
        formula.save()
        
        logger.info(f"Formula {formula.name} activated by {request.user.username}")
        
        return Response({
            'message': f'Formula {formula.name} activated successfully',
            'formula': self.get_serializer(formula).data
        })
    
    @action(detail=True, methods=['post'])
    def duplicate(self, request, pk=None):
        """Duplicate a formula to create a new version"""
        original = self.get_object()
        
        # Create a new formula based on the original
        new_formula = CalculationFormula.objects.create(
            formula_type=original.formula_type,
            name=f"{original.name} (Copy)",
            description=original.description,
            formula_expression=original.formula_expression,
            variables=original.variables,
            weights=original.weights,
            thresholds=original.thresholds,
            is_active=False,
            version=original.version + 1,
            created_by=request.user,
            updated_by=request.user,
            change_notes=f"Duplicated from version {original.version}"
        )
        
        logger.info(f"Formula duplicated by {request.user.username}: {new_formula.name}")
        
        return Response({
            'message': 'Formula duplicated successfully',
            'formula': self.get_serializer(new_formula).data
        }, status=status.HTTP_201_CREATED)


class CalculationBreakdownViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for viewing calculation breakdowns.
    Read-only for all authenticated users.
    """
    queryset = CalculationBreakdown.objects.all()
    serializer_class = CalculationBreakdownSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['calculation_type', 'reference_id']
    ordering_fields = ['calculated_at', 'final_value']
    ordering = ['-calculated_at']
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return CalculationBreakdownDetailSerializer
        return CalculationBreakdownSerializer
    
    @action(detail=False, methods=['get'])
    def by_reference(self, request):
        """Get breakdowns by reference ID"""
        reference_id = request.query_params.get('reference_id')
        calculation_type = request.query_params.get('type')
        
        if not reference_id:
            return Response(
                {'error': 'Reference ID parameter is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        queryset = self.queryset.filter(reference_id=reference_id)
        
        if calculation_type:
            queryset = queryset.filter(calculation_type=calculation_type)
        
        # Get the most recent breakdown
        breakdown = queryset.first()
        
        if not breakdown:
            return Response(
                {'error': 'No breakdown found for the given reference'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = CalculationBreakdownDetailSerializer(breakdown)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_type(self, request):
        """Get all breakdowns by calculation type"""
        calculation_type = request.query_params.get('type')
        
        if not calculation_type:
            return Response(
                {'error': 'Calculation type parameter is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        queryset = self.queryset.filter(calculation_type=calculation_type)
        page = self.paginate_queryset(queryset)
        
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
