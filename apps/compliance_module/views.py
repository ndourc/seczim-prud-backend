from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db.models import Q, Avg, Count
from datetime import datetime, timedelta

from .models import ComplianceIndex, ComplianceAssessment, ComplianceRequirement, ComplianceViolation, ComplianceReport
from .serializers import (
    ComplianceIndexSerializer, ComplianceAssessmentSerializer, ComplianceRequirementSerializer,
    ComplianceViolationSerializer, ComplianceReportSerializer, ComplianceDashboardSerializer,
    ComplianceSummarySerializer
)
from apps.core.models import SMI
from apps.auth_module.models import UserProfile

class ComplianceIndexViewSet(viewsets.ModelViewSet):
    """ViewSet for compliance index management"""
    queryset = ComplianceIndex.objects.all()
    serializer_class = ComplianceIndexSerializer
    permission_classes = [permissions.AllowAny]  # TEMP: Auth disabled for testing
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by SMI if provided
        smi_id = self.request.query_params.get('smi_id')
        if smi_id:
            queryset = queryset.filter(smi_id=smi_id)
        
        # Filter by analysis period
        analysis_period = self.request.query_params.get('analysis_period')
        if analysis_period:
            queryset = queryset.filter(analysis_period=analysis_period)
        
        # Filter by period
        period = self.request.query_params.get('period')
        if period:
            try:
                period_date = datetime.strptime(period, '%Y-%m-%d').date()
                queryset = queryset.filter(period=period_date)
            except ValueError:
                pass
        
        return queryset
    
    def perform_create(self, serializer):
        # Check if user has permission to create compliance indices
        user_profile = UserProfile.objects.get(user=self.request.user)
        if user_profile.role not in ['COMPLIANCE_OFFICER', 'ADMIN']:
            raise permissions.PermissionDenied("You don't have permission to create compliance indices")
        
        # Save the instance
        compliance_index = serializer.save()
        
        # Calculate final compliance score
        compliance_index.calculate_final_compliance_score()
        compliance_index.save()
    
    def perform_update(self, serializer):
        # Check if user has permission to update compliance indices
        user_profile = UserProfile.objects.get(user=self.request.user)
        if user_profile.role not in ['COMPLIANCE_OFFICER', 'ADMIN']:
            raise permissions.PermissionDenied("You don't have permission to update compliance indices")
        
        # Save the instance
        compliance_index = serializer.save()
        
        # Recalculate final compliance score
        compliance_index.calculate_final_compliance_score()
        compliance_index.save()
    
    @action(detail=True, methods=['post'])
    def recalculate_score(self, request, pk=None):
        """Recalculate final compliance score"""
        compliance_index = self.get_object()
        
        # Recalculate score
        compliance_index.calculate_final_compliance_score()
        compliance_index.save()
        
        return Response({
            'message': 'Final compliance score recalculated successfully',
            'final_compliance_score': compliance_index.final_compliance_score
        })

class ComplianceAssessmentViewSet(viewsets.ModelViewSet):
    """ViewSet for compliance assessment management"""
    queryset = ComplianceAssessment.objects.all()
    serializer_class = ComplianceAssessmentSerializer
    permission_classes = [permissions.AllowAny]  # TEMP: Auth disabled for testing
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by SMI if provided
        smi_id = self.request.query_params.get('smi_id')
        if smi_id:
            queryset = queryset.filter(smi_id=smi_id)
        
        # Filter by assessment type
        assessment_type = self.request.query_params.get('assessment_type')
        if assessment_type:
            queryset = queryset.filter(assessment_type=assessment_type)
        
        # Filter by status
        status_filter = self.request.query_params.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        return queryset
    
    def perform_create(self, serializer):
        # Check if user has permission to create compliance assessments
        user_profile = UserProfile.objects.get(user=self.request.user)
        if user_profile.role not in ['COMPLIANCE_OFFICER', 'ADMIN']:
            raise permissions.PermissionDenied("You don't have permission to create compliance assessments")
        
        serializer.save()
    
    def perform_update(self, serializer):
        # Check if user has permission to update compliance assessments
        user_profile = UserProfile.objects.get(user=self.request.user)
        if user_profile.role not in ['COMPLIANCE_OFFICER', 'ADMIN']:
            raise permissions.PermissionDenied("You don't have permission to update compliance assessments")
        
        serializer.save()

class ComplianceRequirementViewSet(viewsets.ModelViewSet):
    """ViewSet for compliance requirement management"""
    queryset = ComplianceRequirement.objects.all()
    serializer_class = ComplianceRequirementSerializer
    permission_classes = [permissions.AllowAny]  # TEMP: Auth disabled for testing
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by SMI if provided
        smi_id = self.request.query_params.get('smi_id')
        if smi_id:
            queryset = queryset.filter(smi_id=smi_id)
        
        # Filter by requirement type
        requirement_type = self.request.query_params.get('requirement_type')
        if requirement_type:
            queryset = queryset.filter(requirement_type=requirement_type)
        
        # Filter by priority
        priority = self.request.query_params.get('priority')
        if priority:
            queryset = queryset.filter(priority=priority)
        
        # Filter by compliance status
        is_compliant = self.request.query_params.get('is_compliant')
        if is_compliant is not None:
            is_compliant_bool = is_compliant.lower() == 'true'
            queryset = queryset.filter(is_compliant=is_compliant_bool)
        
        return queryset

class ComplianceViolationViewSet(viewsets.ModelViewSet):
    """ViewSet for compliance violation management"""
    queryset = ComplianceViolation.objects.all()
    serializer_class = ComplianceViolationSerializer
    permission_classes = [permissions.AllowAny]  # TEMP: Auth disabled for testing
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by SMI if provided
        smi_id = self.request.query_params.get('smi_id')
        if smi_id:
            queryset = queryset.filter(smi_id=smi_id)
        
        # Filter by violation type
        violation_type = self.request.query_params.get('violation_type')
        if violation_type:
            queryset = queryset.filter(violation_type=violation_type)
        
        # Filter by severity
        severity = self.request.query_params.get('severity')
        if severity:
            queryset = queryset.filter(severity=severity)
        
        # Filter by investigation status
        investigation_status = self.request.query_params.get('investigation_status')
        if investigation_status:
            queryset = queryset.filter(investigation_status=investigation_status)
        
        return queryset

class ComplianceReportViewSet(viewsets.ModelViewSet):
    """ViewSet for compliance report management"""
    queryset = ComplianceReport.objects.all()
    serializer_class = ComplianceReportSerializer
    permission_classes = [permissions.AllowAny]  # TEMP: Auth disabled for testing
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by SMI if provided
        smi_id = self.request.query_params.get('smi_id')
        if smi_id:
            queryset = queryset.filter(smi_id=smi_id)
        
        # Filter by report type
        report_type = self.request.query_params.get('report_type')
        if report_type:
            queryset = queryset.filter(report_type=report_type)
        
        # Filter by status
        status_filter = self.request.query_params.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        return queryset
    
    def perform_create(self, serializer):
        serializer.save(prepared_by=self.request.user)
    
    @action(detail=False, methods=['get'])
    def dashboard(self, request):
        """Get compliance dashboard data"""
        # Calculate statistics
        total_smis = SMI.objects.count()
        compliant_smis = ComplianceIndex.objects.filter(
            final_compliance_score__gte=80
        ).values('smi').distinct().count()
        non_compliant_smis = ComplianceIndex.objects.filter(
            final_compliance_score__lt=80
        ).values('smi').distinct().count()
        pending_assessments = ComplianceAssessment.objects.filter(
            status='PENDING'
        ).count()
        recent_violations = ComplianceViolation.objects.filter(
            date_identified__gte=timezone.now().date() - timedelta(days=30)
        ).count()
        
        # Get average compliance score
        avg_compliance_score = ComplianceIndex.objects.aggregate(
            Avg('final_compliance_score')
        )['final_compliance_score__avg'] or 0
        
        # Get recent reports
        recent_reports = self.get_queryset().order_by('-report_date')[:10]
        
        dashboard_data = {
            'total_smis': total_smis,
            'compliant_smis': compliant_smis,
            'non_compliant_smis': non_compliant_smis,
            'pending_assessments': pending_assessments,
            'recent_violations': recent_violations,
            'average_compliance_score': round(avg_compliance_score, 2),
            'recent_reports': ComplianceReportSerializer(recent_reports, many=True).data
        }
        
        return Response(dashboard_data)
