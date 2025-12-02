from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db.models import Q, Count
from datetime import datetime, timedelta

from .models import Case, CaseNote, Investigation, AdHocInspection, CaseAttachment, CaseTimeline
from .serializers import (
    CaseSerializer, CaseNoteSerializer, InvestigationSerializer, AdHocInspectionSerializer,
    CaseAttachmentSerializer, CaseTimelineSerializer, CaseSummarySerializer, CaseDashboardSerializer
)
from apps.core.models import SMI
from apps.auth_module.models import UserProfile

class CaseViewSet(viewsets.ModelViewSet):
    """ViewSet for case management"""
    queryset = Case.objects.all()
    serializer_class = CaseSerializer
    permission_classes = [permissions.AllowAny]  # TEMP: Auth disabled for testing
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by SMI if provided
        smi_id = self.request.query_params.get('smi_id')
        if smi_id:
            queryset = queryset.filter(smi_id=smi_id)
        
        # Filter by case type
        case_type = self.request.query_params.get('case_type')
        if case_type:
            queryset = queryset.filter(case_type=case_type)
        
        # Filter by status
        status_filter = self.request.query_params.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        # Filter by priority
        priority = self.request.query_params.get('priority')
        if priority:
            queryset = queryset.filter(priority=priority)
        
        # Filter by assigned user
        assigned_to = self.request.query_params.get('assigned_to')
        if assigned_to:
            queryset = queryset.filter(assigned_to__username=assigned_to)
        
        return queryset
    
    def perform_create(self, serializer):
        # TESTING MODE: bypass role checks and create case
        # Only assign user if authenticated (not AnonymousUser)
        if not serializer.validated_data.get('assigned_to') and self.request.user.is_authenticated:
            serializer.save(assigned_to=self.request.user)
        else:
            serializer.save()
    
    def perform_update(self, serializer):
        # TESTING MODE: bypass role checks and update case
        serializer.save()
    
    @action(detail=False, methods=['get'])
    def dashboard(self, request):
        """Get case management dashboard data"""
        # Calculate statistics
        total_cases = self.get_queryset().count()
        open_cases = self.get_queryset().filter(status='OPEN').count()
        in_progress_cases = self.get_queryset().filter(status='IN_PROGRESS').count()
        resolved_cases = self.get_queryset().filter(status='RESOLVED').count()
        urgent_cases = self.get_queryset().filter(priority='URGENT').count()
        
        # Get recent cases
        recent_cases = self.get_queryset().order_by('-opened_date')[:10]
        
        dashboard_data = {
            'total_cases': total_cases,
            'open_cases': open_cases,
            'in_progress_cases': in_progress_cases,
            'resolved_cases': resolved_cases,
            'urgent_cases': urgent_cases,
            'recent_cases': CaseSerializer(recent_cases, many=True).data
        }
        
        return Response(dashboard_data)
    
    @action(detail=True, methods=['post'])
    def assign_case(self, request, pk=None):
        """Assign a case to a user"""
        case = self.get_object()
        user_id = request.data.get('user_id')
        
        if not user_id:
            return Response({'error': 'User ID is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            from django.contrib.auth.models import User
            user = User.objects.get(id=user_id)
            case.assigned_to = user
            case.status = 'ASSIGNED'
            case.save()
            
            # Create timeline event
            CaseTimeline.objects.create(
                case=case,
                event_type='ASSIGNED',
                description=f'Case assigned to {user.username}',
                user=request.user
            )
            
            return Response({'message': f'Case assigned to {user.username}'})
            
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=True, methods=['post'])
    def update_status(self, request, pk=None):
        """Update case status"""
        case = self.get_object()
        new_status = request.data.get('status')
        
        if not new_status:
            return Response({'error': 'Status is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        if new_status not in dict(Case.STATUS_CHOICES):
            return Response({'error': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)
        
        old_status = case.status
        case.status = new_status
        case.save()
        
        # Create timeline event
        CaseTimeline.objects.create(
            case=case,
            event_type='STATUS_CHANGED',
            description=f'Status changed from {old_status} to {new_status}',
            user=request.user
        )
        
        return Response({'message': f'Case status updated to {new_status}'})

class CaseNoteViewSet(viewsets.ModelViewSet):
    """ViewSet for case notes management"""
    queryset = CaseNote.objects.all()
    serializer_class = CaseNoteSerializer
    permission_classes = [permissions.AllowAny]  # TEMP: Auth disabled for testing
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by case if provided
        case_id = self.request.query_params.get('case_id')
        if case_id:
            queryset = queryset.filter(case_id=case_id)
        
        return queryset
    
    def perform_create(self, serializer):
        # Only save author if user is authenticated
        if self.request.user.is_authenticated:
            serializer.save(author=self.request.user)
        else:
            # For testing without auth, create a default user or skip author
            serializer.save()

class InvestigationViewSet(viewsets.ModelViewSet):
    """ViewSet for investigation management"""
    queryset = Investigation.objects.all()
    serializer_class = InvestigationSerializer
    permission_classes = [permissions.AllowAny]  # TEMP: Auth disabled for testing
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by case if provided
        case_id = self.request.query_params.get('case_id')
        if case_id:
            queryset = queryset.filter(case_id=case_id)
        
        # Filter by investigation type
        investigation_type = self.request.query_params.get('investigation_type')
        if investigation_type:
            queryset = queryset.filter(investigation_type=investigation_type)
        
        return queryset

class AdHocInspectionViewSet(viewsets.ModelViewSet):
    """ViewSet for ad-hoc inspection management"""
    queryset = AdHocInspection.objects.all()
    serializer_class = AdHocInspectionSerializer
    permission_classes = [permissions.AllowAny]  # TEMP: Auth disabled for testing
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by case if provided
        case_id = self.request.query_params.get('case_id')
        if case_id:
            queryset = queryset.filter(case_id=case_id)
        
        # Filter by trigger type
        trigger_type = self.request.query_params.get('trigger_type')
        if trigger_type:
            queryset = queryset.filter(trigger_type=trigger_type)
        
        return queryset

class CaseAttachmentViewSet(viewsets.ModelViewSet):
    """ViewSet for case attachment management"""
    queryset = CaseAttachment.objects.all()
    serializer_class = CaseAttachmentSerializer
    permission_classes = [permissions.AllowAny]  # TEMP: Auth disabled for testing
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by case if provided
        case_id = self.request.query_params.get('case_id')
        if case_id:
            queryset = queryset.filter(case_id=case_id)
        
        return queryset
    
    def perform_create(self, serializer):
        # Only save uploaded_by if user is authenticated
        if self.request.user.is_authenticated:
            serializer.save(uploaded_by=self.request.user)
        else:
            # For testing without auth, skip uploaded_by
            serializer.save()

class CaseTimelineViewSet(viewsets.ModelViewSet):
    """ViewSet for case timeline management"""
    queryset = CaseTimeline.objects.all()
    serializer_class = CaseTimelineSerializer
    permission_classes = [permissions.AllowAny]  # TEMP: Auth disabled for testing
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by case if provided
        case_id = self.request.query_params.get('case_id')
        if case_id:
            queryset = queryset.filter(case_id=case_id)
        
        return queryset
