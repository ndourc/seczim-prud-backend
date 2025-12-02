from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db.models import Q, Count, Avg

from .models import VA_VASP, VirtualAsset, VASPService, VARiskAssessment, VASPCompliance
from .serializers import (
    VA_VASPSerializer, VirtualAssetSerializer, VASPServiceSerializer,
    VARiskAssessmentSerializer, VASPComplianceSerializer,
    VA_VASPSummarySerializer, VA_VASPDashboardSerializer
)
from apps.core.models import SMI
from apps.auth_module.models import UserProfile

class VA_VASPViewSet(viewsets.ModelViewSet):
    """ViewSet for VA/VASP analysis management"""
    queryset = VA_VASP.objects.all()
    serializer_class = VA_VASPSerializer
    permission_classes = [permissions.AllowAny]  # TEMP: Auth disabled for testing
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by SMI if provided
        smi_id = self.request.query_params.get('smi_id')
        if smi_id:
            queryset = queryset.filter(smi_id=smi_id)
        
        # Filter by VA issuer status
        is_va_issuer = self.request.query_params.get('is_va_issuer')
        if is_va_issuer is not None:
            is_va_issuer_bool = is_va_issuer.lower() == 'true'
            queryset = queryset.filter(is_va_issuer=is_va_issuer_bool)
        
        # Filter by VASP status
        is_vasp = self.request.query_params.get('is_vasp')
        if is_vasp is not None:
            is_vasp_bool = is_vasp.lower() == 'true'
            queryset = queryset.filter(is_vasp=is_vasp_bool)
        
        return queryset
    
    def perform_create(self, serializer):
        # TESTING MODE: bypass role checks and create the instance
        va_vasp = serializer.save()
        # Calculate overall VA risk score
        try:
            va_vasp.calculate_overall_va_risk_score()
            va_vasp.save()
        except Exception:
            pass
    
    def perform_update(self, serializer):
        # TESTING MODE: bypass role checks and update the instance
        va_vasp = serializer.save()
        try:
            va_vasp.calculate_overall_va_risk_score()
            va_vasp.save()
        except Exception:
            pass
    
    @action(detail=False, methods=['get'])
    def dashboard(self, request):
        """Get VA/VASP dashboard data"""
        # Calculate statistics
        total_va_issuers = self.get_queryset().filter(is_va_issuer=True).count()
        total_vasps = self.get_queryset().filter(is_vasp=True).count()
        high_risk_entities = self.get_queryset().filter(overall_va_risk_score__gte=70).count()
        
        # Get compliance alerts (entities with low compliance scores)
        compliance_alerts = self.get_queryset().filter(regulatory_compliance__lt=60).count()
        
        # Get recent analyses
        recent_analyses = self.get_queryset().order_by('-analysis_date')[:10]
        
        dashboard_data = {
            'total_va_issuers': total_va_issuers,
            'total_vasps': total_vasps,
            'high_risk_entities': high_risk_entities,
            'compliance_alerts': compliance_alerts,
            'recent_analyses': VA_VASPSerializer(recent_analyses, many=True).data
        }
        
        return Response(dashboard_data)
    
    @action(detail=True, methods=['post'])
    def recalculate_risk_score(self, request, pk=None):
        """Recalculate overall VA risk score"""
        va_vasp = self.get_object()
        
        # Recalculate risk score
        va_vasp.calculate_overall_va_risk_score()
        va_vasp.save()
        
        return Response({
            'message': 'Risk score recalculated successfully',
            'overall_va_risk_score': va_vasp.overall_va_risk_score
        })

class VirtualAssetViewSet(viewsets.ModelViewSet):
    """ViewSet for virtual asset management"""
    queryset = VirtualAsset.objects.all()
    serializer_class = VirtualAssetSerializer
    permission_classes = [permissions.AllowAny]  # TEMP: Auth disabled for testing
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by VA/VASP analysis if provided
        va_vasp_id = self.request.query_params.get('va_vasp_id')
        if va_vasp_id:
            queryset = queryset.filter(va_vasp_analysis_id=va_vasp_id)
        
        # Filter by asset category
        asset_category = self.request.query_params.get('asset_category')
        if asset_category:
            queryset = queryset.filter(asset_category=asset_category)
        
        # Filter by risk level
        risk_level = self.request.query_params.get('risk_level')
        if risk_level:
            queryset = queryset.filter(risk_level=risk_level)
        
        return queryset

class VASPServiceViewSet(viewsets.ModelViewSet):
    """ViewSet for VASP service management"""
    queryset = VASPService.objects.all()
    serializer_class = VASPServiceSerializer
    permission_classes = [permissions.AllowAny]  # TEMP: Auth disabled for testing
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by VA/VASP analysis if provided
        va_vasp_id = self.request.query_params.get('va_vasp_id')
        if va_vasp_id:
            queryset = queryset.filter(va_vasp_analysis_id=va_vasp_id)
        
        # Filter by service type
        service_type = self.request.query_params.get('service_type')
        if service_type:
            queryset = queryset.filter(service_type=service_type)
        
        # Filter by active status
        is_active = self.request.query_params.get('is_active')
        if is_active is not None:
            is_active_bool = is_active.lower() == 'true'
            queryset = queryset.filter(is_active=is_active_bool)
        
        return queryset

class VARiskAssessmentViewSet(viewsets.ModelViewSet):
    """ViewSet for VA risk assessment management"""
    queryset = VARiskAssessment.objects.all()
    serializer_class = VARiskAssessmentSerializer
    permission_classes = [permissions.AllowAny]  # TEMP: Auth disabled for testing
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by VA/VASP analysis if provided
        va_vasp_id = self.request.query_params.get('va_vasp_id')
        if va_vasp_id:
            queryset = queryset.filter(va_vasp_analysis_id=va_vasp_id)
        
        # Filter by risk category
        risk_category = self.request.query_params.get('risk_category')
        if risk_category:
            queryset = queryset.filter(risk_category=risk_category)
        
        # Filter by risk probability
        risk_probability = self.request.query_params.get('risk_probability')
        if risk_probability:
            queryset = queryset.filter(risk_probability=risk_probability)
        
        return queryset

class VASPComplianceViewSet(viewsets.ModelViewSet):
    """ViewSet for VASP compliance management"""
    queryset = VASPCompliance.objects.all()
    serializer_class = VASPComplianceSerializer
    permission_classes = [permissions.AllowAny]  # TEMP: Auth disabled for testing
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by VA/VASP analysis if provided
        va_vasp_id = self.request.query_params.get('va_vasp_id')
        if va_vasp_id:
            queryset = queryset.filter(va_vasp_analysis_id=va_vasp_id)
        
        # Filter by compliance area
        compliance_area = self.request.query_params.get('compliance_area')
        if compliance_area:
            queryset = queryset.filter(compliance_area=compliance_area)
        
        # Filter by compliance status
        compliance_status = self.request.query_params.get('compliance_status')
        if compliance_status:
            queryset = queryset.filter(compliance_status=compliance_status)
        
        # Filter by follow-up required
        follow_up_required = self.request.query_params.get('follow_up_required')
        if follow_up_required is not None:
            follow_up_required_bool = follow_up_required.lower() == 'true'
            queryset = queryset.filter(follow_up_required=follow_up_required_bool)
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def compliance_alerts(self, request):
        """Get compliance alerts for VASPs"""
        # Get non-compliant entities
        non_compliant = self.get_queryset().filter(
            Q(compliance_status='NON_COMPLIANT') | 
            Q(compliance_score__lt=60)
        )
        
        alerts = []
        for compliance in non_compliant:
            alert = {
                'va_vasp_id': str(compliance.va_vasp_analysis.id),
                'smi_name': compliance.va_vasp_analysis.smi.company_name,
                'compliance_area': compliance.compliance_area,
                'compliance_status': compliance.compliance_status,
                'compliance_score': compliance.compliance_score,
                'gaps_identified': compliance.gaps_identified,
                'follow_up_required': compliance.follow_up_required
            }
            alerts.append(alert)
        
        return Response(alerts)
