from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db.models import Q, Count
from datetime import datetime, timedelta

from .models import PrudentialReturn, IncomeStatement, BalanceSheet
from .serializers import (
    PrudentialReturnSerializer, IncomeStatementSerializer, BalanceSheetSerializer,
    PrudentialReturnSummarySerializer, ReturnsDashboardSerializer
)
from apps.core.models import SMI
from apps.auth_module.models import UserProfile

class PrudentialReturnViewSet(viewsets.ModelViewSet):
    """ViewSet for prudential return management"""
    queryset = PrudentialReturn.objects.all()
    serializer_class = PrudentialReturnSerializer
    permission_classes = [permissions.AllowAny]  # TEMP: Auth disabled for testing
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by SMI if provided
        smi_id = self.request.query_params.get('smi_id')
        if smi_id:
            queryset = queryset.filter(smi_id=smi_id)
        
        # Filter by status
        status_filter = self.request.query_params.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        # Filter by reporting period
        reporting_period = self.request.query_params.get('reporting_period')
        if reporting_period:
            try:
                period_date = datetime.strptime(reporting_period, '%Y-%m-%d').date()
                queryset = queryset.filter(reporting_period=period_date)
            except ValueError:
                pass
        
        # Filter by submission date range
        submission_date_from = self.request.query_params.get('submission_date_from')
        if submission_date_from:
            try:
                from_date = datetime.strptime(submission_date_from, '%Y-%m-%d').date()
                queryset = queryset.filter(submission_date__gte=from_date)
            except ValueError:
                pass
        
        submission_date_to = self.request.query_params.get('submission_date_to')
        if submission_date_to:
            try:
                to_date = datetime.strptime(submission_date_to, '%Y-%m-%d').date()
                queryset = queryset.filter(submission_date__lte=to_date)
            except ValueError:
                pass
        
        return queryset
    
    def perform_create(self, serializer):
        # TESTING MODE: bypass role checks and create the return
        serializer.save()
    
    def perform_update(self, serializer):
        # TESTING MODE: bypass role checks and update the return
        serializer.save()
    
    @action(detail=False, methods=['get'])
    def dashboard(self, request):
        """Get returns dashboard data"""
        # Calculate statistics
        total_returns = self.get_queryset().count()
        submitted_returns = self.get_queryset().filter(status='SUBMITTED').count()
        pending_returns = self.get_queryset().filter(status='PENDING').count()
        approved_returns = self.get_queryset().filter(status='APPROVED').count()
        rejected_returns = self.get_queryset().filter(status='REJECTED').count()
        
        # Get recent returns
        recent_returns = self.get_queryset().order_by('-submission_date')[:10]
        
        dashboard_data = {
            'total_returns': total_returns,
            'submitted_returns': submitted_returns,
            'pending_returns': pending_returns,
            'approved_returns': approved_returns,
            'rejected_returns': rejected_returns,
            'recent_returns': PrudentialReturnSerializer(recent_returns, many=True).data
        }
        
        return Response(dashboard_data)
    
    @action(detail=True, methods=['post'])
    def submit_return(self, request, pk=None):
        """Submit a prudential return"""
        prudential_return = self.get_object()
        
        if prudential_return.status != 'DRAFT':
            return Response({'error': 'Only draft returns can be submitted'}, 
                         status=status.HTTP_400_BAD_REQUEST)
        
        prudential_return.status = 'SUBMITTED'
        prudential_return.submission_date = timezone.now().date()
        prudential_return.save()
        
        return Response({'message': 'Return submitted successfully'})
    
    @action(detail=True, methods=['post'])
    def approve_return(self, request, pk=None):
        """Approve a prudential return"""
        prudential_return = self.get_object()
        
        if prudential_return.status != 'SUBMITTED':
            return Response({'error': 'Only submitted returns can be approved'}, 
                         status=status.HTTP_400_BAD_REQUEST)
        
        prudential_return.status = 'APPROVED'
        prudential_return.save()
        
        return Response({'message': 'Return approved successfully'})
    
    @action(detail=True, methods=['post'])
    def reject_return(self, request, pk=None):
        """Reject a prudential return"""
        prudential_return = self.get_object()
        
        if prudential_return.status != 'SUBMITTED':
            return Response({'error': 'Only submitted returns can be rejected'}, 
                         status=status.HTTP_400_BAD_REQUEST)
        
        reason = request.data.get('reason', '')
        if not reason:
            return Response({'error': 'Rejection reason is required'}, 
                         status=status.HTTP_400_BAD_REQUEST)
        
        prudential_return.status = 'REJECTED'
        prudential_return.notes = reason
        prudential_return.save()
        
        return Response({'message': 'Return rejected successfully'})

class IncomeStatementViewSet(viewsets.ModelViewSet):
    """ViewSet for income statement management"""
    queryset = IncomeStatement.objects.all()
    serializer_class = IncomeStatementSerializer
    permission_classes = [permissions.AllowAny]  # TEMP: Auth disabled for testing
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by prudential return if provided
        prudential_return_id = self.request.query_params.get('prudential_return_id')
        if prudential_return_id:
            queryset = queryset.filter(prudential_return_id=prudential_return_id)
        
        return queryset

class BalanceSheetViewSet(viewsets.ModelViewSet):
    """ViewSet for balance sheet management"""
    queryset = BalanceSheet.objects.all()
    serializer_class = BalanceSheetSerializer
    permission_classes = [permissions.AllowAny]  # TEMP: Auth disabled for testing
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by prudential return if provided
        prudential_return_id = self.request.query_params.get('prudential_return_id')
        if prudential_return_id:
            queryset = queryset.filter(prudential_return_id=prudential_return_id)
        
        return queryset
