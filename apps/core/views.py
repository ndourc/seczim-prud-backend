from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models import Max
from django.contrib.auth import authenticate
import logging

from .models import (
    SMI, BoardMember, MeetingLog, ProductOffering, ClienteleProfile,
    FinancialStatement, ClientAssetMix, LicensingBreach, SupervisoryIntervention,
    Notification, SystemAuditLog
)
from .serializers import (
    SMISerializer, BoardMemberSerializer, MeetingLogSerializer, ProductOfferingSerializer,
    ClienteleProfileSerializer, FinancialStatementSerializer, ClientAssetMixSerializer,
    LicensingBreachSerializer, SupervisoryInterventionSerializer,
    NotificationSerializer, SystemAuditLogSerializer, SMIDetailSerializer,
    SMIDashboardSerializer
)
from apps.auth_module.permissions import (
    IsAdminUser, IsPrincipalOfficer, IsAccountant, IsComplianceOfficer,
    CanViewSmiData, CanEditSmiData, CanViewReports, CanCreateReports
)

logger = logging.getLogger(__name__)

class SMIViewSet(viewsets.ModelViewSet):
    """
    ViewSet for SMI (Supervised Market Intermediary) management
    """
    queryset = SMI.objects.all()
    serializer_class = SMISerializer
    permission_classes = [permissions.AllowAny]  # AUTH_DISABLED - was: IsAuthenticated, CanViewSmiData
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['company_name', 'license_number', 'email', 'phone']
    ordering_fields = ['company_name', 'registration_date', 'created_at']
    ordering = ['company_name']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return SMIDetailSerializer
        elif self.action == 'dashboard':
            return SMIDashboardSerializer
        return SMISerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), CanEditSmiData()]
        return super().get_permissions()

    @action(detail=False, methods=['get'])
    def dashboard(self, request):
        """Get SMI dashboard data with summary information"""
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def risk_profile(self, request, pk=None):
        """Get comprehensive risk profile for an SMI"""
        smi = self.get_object()
        
        data = {
            'smi': SMISerializer(smi).data,
            'message': 'Risk assessment data is available through the risk assessment module API'
        }
        return Response(data)

    @action(detail=True, methods=['get'])
    def financial_summary(self, request, pk=None):
        """Get financial summary for an SMI"""
        smi = self.get_object()
        financial_statements = smi.financial_statements.order_by('-period')
        
        data = {
            'smi': SMISerializer(smi).data,
            'financial_statements': FinancialStatementSerializer(financial_statements, many=True).data,
            'total_assets': financial_statements.aggregate(Max('total_assets'))['total_assets__max'],
            'total_revenue': financial_statements.aggregate(Max('total_revenue'))['total_revenue__max'],
        }
        return Response(data)

    @action(detail=False, methods=['get'])
    def summary(self, request):
        """Get summary statistics for all SMIs"""
        total_smis = SMI.objects.count()
        active_smis = SMI.objects.filter(status='ACTIVE').count()
        suspended_smis = SMI.objects.filter(status='SUSPENDED').count()
        
        data = {
            'count': total_smis,
            'active': active_smis,
            'suspended': suspended_smis,
            'total': total_smis
        }
        return Response(data)

class BoardMemberViewSet(viewsets.ModelViewSet):
    queryset = BoardMember.objects.all()
    serializer_class = BoardMemberSerializer
    permission_classes = [permissions.AllowAny]  # AUTH_DISABLED - was: IsAuthenticated, CanViewSmiData
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'position', 'smi__company_name']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), CanEditSmiData()]
        return super().get_permissions()

class MeetingLogViewSet(viewsets.ModelViewSet):
    queryset = MeetingLog.objects.all()
    serializer_class = MeetingLogSerializer
    permission_classes = [permissions.AllowAny]  # AUTH_DISABLED - was: IsAuthenticated, CanViewSmiData
    filter_backends = [filters.SearchFilter]
    search_fields = ['smi__company_name', 'agenda', 'decisions']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), CanEditSmiData()]
        return super().get_permissions()

class ProductOfferingViewSet(viewsets.ModelViewSet):
    queryset = ProductOffering.objects.all()
    serializer_class = ProductOfferingSerializer
    permission_classes = [permissions.AllowAny]  # AUTH_DISABLED - was: IsAuthenticated, CanViewSmiData
    filter_backends = [filters.SearchFilter]
    search_fields = ['product_name', 'smi__company_name']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), CanEditSmiData()]
        return super().get_permissions()

class ClienteleProfileViewSet(viewsets.ModelViewSet):
    queryset = ClienteleProfile.objects.all()
    serializer_class = ClienteleProfileSerializer
    permission_classes = [permissions.AllowAny]  # AUTH_DISABLED - was: IsAuthenticated, CanViewSmiData
    filter_backends = [filters.SearchFilter]
    search_fields = ['smi__company_name']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), CanEditSmiData()]
        return super().get_permissions()

class FinancialStatementViewSet(viewsets.ModelViewSet):
    queryset = FinancialStatement.objects.all()
    serializer_class = FinancialStatementSerializer
    permission_classes = [permissions.AllowAny]  # AUTH_DISABLED - was: IsAuthenticated, CanViewSmiData
    filter_backends = [filters.SearchFilter]
    search_fields = ['smi__company_name']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), CanEditSmiData()]
        return super().get_permissions()

class ClientAssetMixViewSet(viewsets.ModelViewSet):
    queryset = ClientAssetMix.objects.all()
    serializer_class = ClientAssetMixSerializer
    permission_classes = [permissions.AllowAny]  # AUTH_DISABLED - was: IsAuthenticated, CanViewSmiData
    filter_backends = [filters.SearchFilter]
    search_fields = ['smi__company_name']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), CanEditSmiData()]
        return super().get_permissions()

class LicensingBreachViewSet(viewsets.ModelViewSet):
    queryset = LicensingBreach.objects.all()
    serializer_class = LicensingBreachSerializer
    permission_classes = [permissions.AllowAny]  # AUTH_DISABLED - was: IsAuthenticated, CanViewReports
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['smi__company_name', 'assigned_to__username', 'description']
    ordering_fields = ['breach_date', 'created_at']
    ordering = ['-breach_date']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), CanCreateReports()]
        return super().get_permissions()

class SupervisoryInterventionViewSet(viewsets.ModelViewSet):
    queryset = SupervisoryIntervention.objects.all()
    serializer_class = SupervisoryInterventionSerializer
    permission_classes = [permissions.AllowAny]  # AUTH_DISABLED - was: IsAuthenticated, CanViewReports
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['smi__company_name', 'reason', 'description']
    ordering_fields = ['intervention_date', 'created_at']
    ordering = ['-intervention_date']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), CanCreateReports()]
        return super().get_permissions()

class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [permissions.AllowAny]  # TEMP: Auth disabled for testing
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'message']
    ordering_fields = ['created_at', 'priority']
    ordering = ['-created_at']

    def get_queryset(self):
        # Short-circuit for Swagger schema generation
        if getattr(self, 'swagger_fake_view', False):
            return Notification.objects.none()
        
        return Notification.objects.filter(user=self.request.user)

    @action(detail=True, methods=['post'])
    def mark_read(self, request, pk=None):
        """Mark a notification as read"""
        notification = self.get_object()
        notification.read = True
        notification.read_at = timezone.now()
        notification.save()
        return Response({'status': 'marked as read'})

    @action(detail=False, methods=['post'])
    def mark_all_read(self, request):
        """Mark all notifications as read"""
        self.get_queryset().update(read=True, read_at=timezone.now())
        return Response({'status': 'all marked as read'})

class SystemAuditLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SystemAuditLog.objects.all()
    serializer_class = SystemAuditLogSerializer
    permission_classes = [permissions.AllowAny]  # AUTH_DISABLED - was: IsAuthenticated, IsAdminUser
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['action', 'model_name', 'object_repr', 'user__username']
    ordering_fields = ['timestamp']
    ordering = ['-timestamp']
