from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db import transaction
import requests
import logging

from .models import (
    LicensingPortalIntegration, PortalSMIData, InstitutionalProfile,
    Shareholder, Director, LicenseHistory
)
from .serializers import (
    LicensingPortalIntegrationSerializer, PortalSMIDataSerializer,
    InstitutionalProfileSerializer, ShareholderSerializer,
    DirectorSerializer, LicenseHistorySerializer,
    SMIInstitutionalDataSerializer, LicensingPortalSyncSerializer,
    PortalDataUpdateSerializer
)
from apps.core.models import SMI
from apps.auth_module.models import UserProfile

logger = logging.getLogger(__name__)

class LicensingPortalIntegrationViewSet(viewsets.ModelViewSet):
    """ViewSet for licensing portal integration management"""
    queryset = LicensingPortalIntegration.objects.all()
    serializer_class = LicensingPortalIntegrationSerializer
    permission_classes = [permissions.AllowAny]  # TEMP: Auth disabled for testing
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAdminUser]
        return super().get_permissions()
    
    @action(detail=True, methods=['post'])
    def test_connection(self, request, pk=None):
        """Test connection to licensing portal"""
        integration = self.get_object()
        
        try:
            # Test API connection
            response = requests.get(
                f"{integration.api_endpoint}/health",
                headers={'Authorization': f'Bearer {integration.api_key}'} if integration.api_key else {},
                timeout=10
            )
            
            if response.status_code == 200:
                integration.status = 'ACTIVE'
                integration.sync_errors = ''
                integration.save()
                return Response({'status': 'Connection successful', 'portal_status': 'ACTIVE'})
            else:
                integration.status = 'ERROR'
                integration.sync_errors = f"HTTP {response.status_code}: {response.text}"
                integration.save()
                return Response({'status': 'Connection failed', 'error': response.text}, 
                             status=status.HTTP_400_BAD_REQUEST)
                
        except Exception as e:
            integration.status = 'ERROR'
            integration.sync_errors = str(e)
            integration.save()
            logger.error(f"Portal connection error: {e}")
            return Response({'status': 'Connection failed', 'error': str(e)}, 
                         status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'])
    def sync_data(self, request, pk=None):
        """Manually trigger data synchronization"""
        integration = self.get_object()
        
        if integration.status != 'ACTIVE':
            return Response({'error': 'Portal integration is not active'}, 
                         status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Trigger sync process
            # This would typically be handled by a Celery task
            integration.last_sync = timezone.now()
            integration.save()
            
            return Response({'status': 'Sync initiated', 'last_sync': integration.last_sync})
            
        except Exception as e:
            logger.error(f"Sync error: {e}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class PortalSMIDataViewSet(viewsets.ModelViewSet):
    """ViewSet for portal SMI data management"""
    queryset = PortalSMIData.objects.all()
    serializer_class = PortalSMIDataSerializer
    permission_classes = [permissions.AllowAny]  # TEMP: Auth disabled for testing
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by SMI if provided
        smi_id = self.request.query_params.get('smi_id')
        if smi_id:
            queryset = queryset.filter(smi_id=smi_id)
        
        # Filter by sync status
        sync_status = self.request.query_params.get('sync_status')
        if sync_status:
            queryset = queryset.filter(sync_status=sync_status)
        
        return queryset
    
    @action(detail=False, methods=['post'])
    def update_portal_data(self, request):
        """Update portal data for an SMI"""
        serializer = PortalDataUpdateSerializer(data=request.data)
        if serializer.is_valid():
            try:
                portal_data = PortalSMIData.objects.get(
                    portal_id=serializer.validated_data['portal_id']
                )
                
                # Update fields if provided
                for field, value in serializer.validated_data.items():
                    if field != 'portal_id' and hasattr(portal_data, field):
                        setattr(portal_data, field, value)
                
                portal_data.sync_status = 'SYNCED'
                portal_data.last_updated_from_portal = timezone.now()
                portal_data.save()
                
                return Response(PortalSMIDataSerializer(portal_data).data)
                
            except PortalSMIData.DoesNotExist:
                return Response({'error': 'Portal data not found'}, 
                             status=status.HTTP_404_NOT_FOUND)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class InstitutionalProfileViewSet(viewsets.ModelViewSet):
    """ViewSet for institutional profile management"""
    queryset = InstitutionalProfile.objects.all()
    serializer_class = InstitutionalProfileSerializer
    permission_classes = [permissions.AllowAny]  # TEMP: Auth disabled for testing
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by SMI if provided
        smi_id = self.request.query_params.get('smi_id')
        if smi_id:
            queryset = queryset.filter(smi_id=smi_id)
        
        # Filter by competitive position
        competitive_position = self.request.query_params.get('competitive_position')
        if competitive_position:
            queryset = queryset.filter(competitive_position=competitive_position)
        
        return queryset
    
    def perform_create(self, serializer):
        # TESTING MODE: bypass role checks and create institutional profile
        serializer.save()
    
    def perform_update(self, serializer):
        # TESTING MODE: bypass role checks and update institutional profile
        serializer.save()

class ShareholderViewSet(viewsets.ModelViewSet):
    """ViewSet for shareholder management"""
    queryset = Shareholder.objects.all()
    serializer_class = ShareholderSerializer
    permission_classes = [permissions.AllowAny]  # TEMP: Auth disabled for testing
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by SMI if provided
        smi_id = self.request.query_params.get('smi_id')
        if smi_id:
            queryset = queryset.filter(smi_id=smi_id)
        
        # Filter by shareholder type
        shareholder_type = self.request.query_params.get('shareholder_type')
        if shareholder_type:
            queryset = queryset.filter(shareholder_type=shareholder_type)
        
        return queryset
    
    def perform_create(self, serializer):
        # TESTING MODE: bypass role checks and create shareholder
        serializer.save()
    
    def perform_update(self, serializer):
        # TESTING MODE: bypass role checks and update shareholder
        serializer.save()

class DirectorViewSet(viewsets.ModelViewSet):
    """ViewSet for director management"""
    queryset = Director.objects.all()
    serializer_class = DirectorSerializer
    permission_classes = [permissions.AllowAny]  # TEMP: Auth disabled for testing
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by SMI if provided
        smi_id = self.request.query_params.get('smi_id')
        if smi_id:
            queryset = queryset.filter(smi_id=smi_id)
        
        # Filter by director type
        director_type = self.request.query_params.get('director_type')
        if director_type:
            queryset = queryset.filter(director_type=director_type)
        
        # Filter by active status
        is_active = self.request.query_params.get('is_active')
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active.lower() == 'true')
        
        return queryset
    
    def perform_create(self, serializer):
        # TESTING MODE: bypass role checks and create director
        serializer.save()
    
    def perform_update(self, serializer):
        # TESTING MODE: bypass role checks and update director
        serializer.save()

class LicenseHistoryViewSet(viewsets.ModelViewSet):
    """ViewSet for license history management"""
    queryset = LicenseHistory.objects.all()
    serializer_class = LicenseHistorySerializer
    permission_classes = [permissions.AllowAny]  # TEMP: Auth disabled for testing
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by SMI if provided
        smi_id = self.request.query_params.get('smi_id')
        if smi_id:
            queryset = queryset.filter(smi_id=smi_id)
        
        # Filter by change type
        change_type = self.request.query_params.get('change_type')
        if change_type:
            queryset = queryset.filter(change_type=change_type)
        
        # Filter by active status
        is_active = self.request.query_params.get('is_active')
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active.lower() == 'true')
        
        return queryset

class LicensingPortalSyncViewSet(viewsets.ViewSet):
    """ViewSet for licensing portal synchronization operations"""
    permission_classes = [permissions.AllowAny]  # TEMP: Auth disabled for testing
    
    @action(detail=False, methods=['post'])
    def sync_smi_data(self, request):
        """Synchronize SMI data from licensing portal"""
        serializer = LicensingPortalSyncSerializer(data=request.data)
        if serializer.is_valid():
            smi_id = serializer.validated_data['smi_id']
            sync_type = serializer.validated_data['sync_type']
            force_sync = serializer.validated_data['force_sync']
            
            try:
                smi = SMI.objects.get(id=smi_id)
                
                # Check if portal integration is active
                portal_integration = LicensingPortalIntegration.objects.filter(status='ACTIVE').first()
                if not portal_integration:
                    return Response({'error': 'No active portal integration found'}, 
                                 status=status.HTTP_400_BAD_REQUEST)
                
                # Perform sync based on type
                if sync_type == 'FULL':
                    # Full sync - would typically be handled by Celery task
                    result = self._perform_full_sync(smi, portal_integration)
                elif sync_type == 'INCREMENTAL':
                    result = self._perform_incremental_sync(smi, portal_integration)
                else:  # SELECTIVE
                    result = self._perform_selective_sync(smi, portal_integration)
                
                return Response(result)
                
            except SMI.DoesNotExist:
                return Response({'error': 'SMI not found'}, 
                             status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                logger.error(f"Sync error: {e}")
                return Response({'error': str(e)}, 
                             status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def _perform_full_sync(self, smi, portal_integration):
        """Perform full synchronization of SMI data"""
        # This would typically call the licensing portal API
        # and update all related models
        
        # For now, return a placeholder response
        return {
            'status': 'Full sync initiated',
            'smi_id': str(smi.id),
            'sync_type': 'FULL',
            'timestamp': timezone.now().isoformat()
        }
    
    def _perform_incremental_sync(self, smi, portal_integration):
        """Perform incremental synchronization of SMI data"""
        # This would typically check for changes since last sync
        return {
            'status': 'Incremental sync initiated',
            'smi_id': str(smi.id),
            'sync_type': 'INCREMENTAL',
            'timestamp': timezone.now().isoformat()
        }
    
    def _perform_selective_sync(self, smi, portal_integration):
        """Perform selective synchronization of specific SMI data"""
        # This would typically sync only specific data fields
        return {
            'status': 'Selective sync initiated',
            'smi_id': str(smi.id),
            'sync_type': 'SELECTIVE',
            'timestamp': timezone.now().isoformat()
        }

