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
    SMIDashboardSerializer, OffsiteProfilingSerializer
)
from apps.auth_module.permissions import (
    IsAdminUser, IsPrincipalOfficer, IsAccountant, IsComplianceOfficer,
    CanViewSmiData, CanEditSmiData, CanViewReports, CanCreateReports
)

logger = logging.getLogger(__name__)

from .mixins import AuditLogMixin

class SMIViewSet(AuditLogMixin, viewsets.ModelViewSet):
    """
    ViewSet for SMI (Supervised Market Intermediary) management
    """
    queryset = SMI.objects.all()
    serializer_class = SMISerializer
    permission_classes = [permissions.AllowAny]
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
        return [permissions.AllowAny()]

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

class BoardMemberViewSet(AuditLogMixin, viewsets.ModelViewSet):
    queryset = BoardMember.objects.all()
    serializer_class = BoardMemberSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'position', 'smi__company_name']

    def get_permissions(self):
        return [permissions.AllowAny()]

class MeetingLogViewSet(AuditLogMixin, viewsets.ModelViewSet):
    queryset = MeetingLog.objects.all()
    serializer_class = MeetingLogSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.SearchFilter]
    search_fields = ['smi__company_name', 'agenda', 'decisions']

    def get_permissions(self):
        return [permissions.AllowAny()]

class ProductOfferingViewSet(AuditLogMixin, viewsets.ModelViewSet):
    queryset = ProductOffering.objects.all()
    serializer_class = ProductOfferingSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.SearchFilter]
    search_fields = ['product_name', 'smi__company_name']

    def get_permissions(self):
        return [permissions.AllowAny()]

class ClienteleProfileViewSet(AuditLogMixin, viewsets.ModelViewSet):
    queryset = ClienteleProfile.objects.all()
    serializer_class = ClienteleProfileSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.SearchFilter]
    search_fields = ['smi__company_name']

    def get_permissions(self):
        return [permissions.AllowAny()]

class FinancialStatementViewSet(AuditLogMixin, viewsets.ModelViewSet):
    queryset = FinancialStatement.objects.all()
    serializer_class = FinancialStatementSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.SearchFilter]
    search_fields = ['smi__company_name']

    def get_permissions(self):
        return [permissions.AllowAny()]

class ClientAssetMixViewSet(AuditLogMixin, viewsets.ModelViewSet):
    queryset = ClientAssetMix.objects.all()
    serializer_class = ClientAssetMixSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.SearchFilter]
    search_fields = ['smi__company_name']

    def get_permissions(self):
        return [permissions.AllowAny()]

class LicensingBreachViewSet(AuditLogMixin, viewsets.ModelViewSet):
    queryset = LicensingBreach.objects.all()
    serializer_class = LicensingBreachSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['smi__company_name', 'assigned_to__username', 'description']
    ordering_fields = ['breach_date', 'created_at']
    ordering = ['-breach_date']

    def get_permissions(self):
        return [permissions.AllowAny()]

class SupervisoryInterventionViewSet(AuditLogMixin, viewsets.ModelViewSet):
    queryset = SupervisoryIntervention.objects.all()
    serializer_class = SupervisoryInterventionSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['smi__company_name', 'reason', 'description']
    ordering_fields = ['intervention_date', 'created_at']
    ordering = ['-intervention_date']

    def get_permissions(self):
        return [permissions.AllowAny()]

class NotificationViewSet(AuditLogMixin, viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'message']
    ordering_fields = ['created_at', 'priority']
    ordering = ['-created_at']

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Notification.objects.none()
        if self.request.user.is_anonymous:
            return Notification.objects.all()
        return Notification.objects.filter(user=self.request.user)

    @action(detail=True, methods=['post'])
    def mark_read(self, request, pk=None):
        notification = self.get_object()
        notification.read = True
        notification.read_at = timezone.now()
        notification.save()
        return Response({'status': 'marked as read'})

    @action(detail=False, methods=['post'])
    def mark_all_read(self, request):
        self.get_queryset().update(read=True, read_at=timezone.now())
        return Response({'status': 'all marked as read'})

class SystemAuditLogViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ReadOnly viewset for audit logs - we don't audit the audit logs themselves
    """
    queryset = SystemAuditLog.objects.all()
    serializer_class = SystemAuditLogSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['action', 'model_name', 'object_repr', 'user__username']
    ordering_fields = ['timestamp']
    ordering = ['-timestamp']

class OffsiteProfilingViewSet(viewsets.ViewSet):
    """
    ViewSet for handling Offsite Profiling submissions
    """
    permission_classes = [permissions.AllowAny]

    def create(self, request):
        serializer = OffsiteProfilingSerializer(data=request.data)
        if serializer.is_valid():
            # Use transaction to ensure atomicity
            from django.db import transaction
            
            try:
                with transaction.atomic():
                    # Call save manually or delegate to serializer if logic moved there?
                    # The serializer.save() currently does logic in create() of serializer.
                    # We need to override that or modify the serializer. create() in ViewSet blindly calls save().
                    # Let's modify the SERIALIZER's create method, not the VIEW's create method logic directly if possible,
                    # BUT `serializer.save()` calls `serializer.create()`.
                    # So I should strictly be modifying `apps/core/serializers.py`.
                    serializer.save()

                return Response({'status': 'success', 'message': 'Offsite profiling data submitted successfully'}, status=status.HTTP_201_CREATED)
            except Exception as e:
                # Log full exception with stack for debugging
                logger.exception("Offsite profiling save failed: %s", e)

                # Attempt to scan validated_data for suspicious date-like or smart-quote values
                try:
                    vd = getattr(serializer, 'validated_data', None)
                    def scan(obj, path=''):
                        findings = []
                        if isinstance(obj, dict):
                            for k, v in obj.items():
                                p = f"{path}.{k}" if path else k
                                findings.extend(scan(v, p))
                        elif isinstance(obj, list):
                            for idx, item in enumerate(obj):
                                p = f"{path}[{idx}]"
                                findings.extend(scan(item, p))
                        else:
                            if isinstance(obj, str):
                                # look for smart quotes or non-ASCII quote characters
                                if any(c in obj for c in ['“', '”', '‘', '’']):
                                    findings.append((path, obj))
                                # look for values that are just quotes
                                if obj.strip() in ['""', "''", '“”', '‘’']:
                                    findings.append((path, obj))
                        return findings

                    if vd:
                        suspicious = scan(vd)
                        if suspicious:
                            for p, val in suspicious:
                                logger.error("Suspicious value at %s: %r", p, val)
                        else:
                            logger.error("No suspicious smart-quote strings found in validated_data")
                except Exception:
                    logger.exception("Failed scanning validated_data for suspicious values")

                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
                
        # Log validation errors and parsed request data for debugging
        try:
            logger.error("Offsite profiling validation failed: %s", serializer.errors)
            # request.data is already parsed by DRF and safe to log
            try:
                logger.error("Offsite profiling request.data: %s", request.data)
            except Exception:
                logger.exception("Failed to log request.data for offsite profiling")
        except Exception as log_exc:
            logger.exception("Failed to log offsite profiling validation error: %s", log_exc)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """
        Retrieve aggregated profile data for an SMI (pk=smi_id)
        """
        smi_id = pk
        try:
            smi = SMI.objects.get(id=smi_id)
        except SMI.DoesNotExist:
            return Response({'error': 'SMI not found'}, status=status.HTTP_404_NOT_FOUND)

        # 1. Board Members
        board_members = BoardMember.objects.filter(smi=smi).values(
            'name', 'position', 'appointment_date'
        )
        # Rename keys to match frontend expectation
        bm_data = [
            {
                'name': bm['name'],
                'position': bm['position'],
                'appointmentDate': bm['appointment_date']
            } for bm in board_members
        ]

        # 2. Committees (assuming Committee model exists and is linked)
        # The serializer uses Committee model, need to import it if not already imported in views
        from .models import Committee
        committees = Committee.objects.filter(smi=smi)
        comm_data = [
            {
                'name': c.name,
                'purpose': c.purpose,
                'chairperson': c.chairperson,
                'members': c.members,
                'meetingsHeld': c.meetings_held,
                'meetingFrequency': c.meeting_frequency
            } for c in committees
        ]

        # 3. Products
        products = ProductOffering.objects.filter(smi=smi)
        prod_data = [
            {
                'productName': p.product_name,
                'productType': p.product_category,
                'concentrationPercentage': p.income_contribution 
            } for p in products
        ]

        # 4. Clients
        clients = ClienteleProfile.objects.filter(smi=smi)
        client_data = [
            {
                'clientType': c.client_type,
                'concentrationPercentage': c.income_contribution
            } for c in clients
        ]

        # 5. Financial Statements (Income & Position)
        # Get latest ones or list? Frontend form implies single period editing usually.
        # Let's try to find the most recent ones.
        
        # Income Statement
        income_stmt = FinancialStatement.objects.filter(
            smi=smi, statement_type='COMPREHENSIVE_INCOME'
        ).order_by('-period').first()

        fs_data = {
            'periodStart': '', # Not stored in model directly? Model has 'period' (end date).
            'periodEnd': income_stmt.period if income_stmt else '',
            'totalRevenue': income_stmt.total_revenue if income_stmt else 0,
            'operatingCosts': income_stmt.total_expenses if income_stmt else 0,
            'profitBeforeTax': income_stmt.profit_before_tax if income_stmt else 0,
            'grossMargin': income_stmt.gross_margin if income_stmt else 0,
            'profitMargin': income_stmt.profit_margin if income_stmt else 0,
            'incomeItems': []
        }
        if income_stmt:
            from .models import IncomeItem
            income_items = IncomeItem.objects.filter(financial_statement=income_stmt)
            fs_data['incomeItems'] = [
                {
                    'category': i.category,
                    'description': i.description,
                    'amount': i.amount,
                    'isCore': i.is_core
                } for i in income_items
            ]

        # Balance Sheet
        pos_stmt = FinancialStatement.objects.filter(
            smi=smi, statement_type='FINANCIAL_POSITION'
        ).order_by('-period').first()

        bs_data = {
            'periodEnd': pos_stmt.period if pos_stmt else '',
            'totalAssets': pos_stmt.total_assets if pos_stmt else 0,
            'totalLiabilities': pos_stmt.total_liabilities if pos_stmt else 0,
            'shareholdersFunds': pos_stmt.total_equity if pos_stmt else 0,
            'currentAssets': 0, # Calculated fields need logic or storage?
            'currentLiabilities': 0,
            'assets': [],
            'liabilities': [],
            'debtors': [],
            'creditors': [],
            'relatedParties': []
        }

        if pos_stmt:
            from .models import Asset, Liability, Debtor, Creditor, RelatedParty
            
            assets = Asset.objects.filter(financial_statement=pos_stmt)
            bs_data['assets'] = [
                {
                    'assetType': a.asset_type,
                    'category': a.category,
                    'value': a.value,
                    'isCurrent': a.is_current,
                    'acquisitionDate': a.acquisition_date
                } for a in assets
            ]
            # Calculate current assets
            bs_data['currentAssets'] = sum(a.value for a in assets if a.is_current)

            liabilities = Liability.objects.filter(financial_statement=pos_stmt)
            bs_data['liabilities'] = [
                {
                    'liabilityType': a.liability_type,
                    'category': a.category,
                    'value': a.value,
                    'isCurrent': a.is_current,
                    'dueDate': a.due_date
                } for a in liabilities
            ]
            # Calculate current liabilities
            bs_data['currentLiabilities'] = sum(a.value for a in liabilities if a.is_current)

            debtors = Debtor.objects.filter(financial_statement=pos_stmt)
            bs_data['debtors'] = [
                {
                    'name': d.name,
                    'amount': d.amount,
                    'ageDays': d.age_days
                } for d in debtors
            ]

            creditors = Creditor.objects.filter(financial_statement=pos_stmt)
            bs_data['creditors'] = [
                {
                    'name': c.name,
                    'amount': c.amount,
                    'dueDate': c.due_date
                } for c in creditors
            ]

            related = RelatedParty.objects.filter(financial_statement=pos_stmt)
            bs_data['relatedParties'] = [
                {
                    'name': r.name,
                    'relationship': r.relationship,
                    'balance': r.balance,
                    'type': r.transaction_type
                } for r in related
            ]

        # 6. Client Assets (ClientAssetMix)
        client_assets = ClientAssetMix.objects.filter(smi=smi).order_by('-period')
        # Maybe filter by latest period? Assuming all belong to same submission for now
        ca_data = [
            {
                'assetType': ca.asset_class,
                'concentrationPercentage': ca.allocation_percentage,
                'value': ca.market_value
            } for ca in client_assets
        ]

        # 7. Capital Position
        from .models import CapitalPosition
        cap_pos = CapitalPosition.objects.filter(smi=smi).order_by('-calculation_date').first()
        cp_data = {
            'calculationDate': cap_pos.calculation_date if cap_pos else '',
            'netCapital': cap_pos.net_capital if cap_pos else 0,
            'requiredCapital': cap_pos.required_capital if cap_pos else 0,
            'adjustedLiquidCapital': cap_pos.adjusted_liquid_capital if cap_pos else 0,
            'isCompliant': cap_pos.is_compliant if cap_pos else False,
            'capitalAdequacyRatio': cap_pos.capital_adequacy_ratio if cap_pos else 0
        }

        response_data = {
            'companyId': str(smi.id),
            'reportingPeriod': {
                'start': fs_data['periodStart'] or '', # Fallback
                'end': fs_data['periodEnd'] or bs_data['periodEnd'] or ''
            },
            'boardMembers': bm_data,
            'committees': comm_data,
            'products': prod_data,
            'clients': client_data,
            'financialStatement': fs_data,
            'balanceSheet': bs_data,
            'clientAssets': ca_data,
            'capitalPosition': cp_data,
            'supportingDocuments': [] # File handling is complex, skip for now
        }

        return Response(response_data)
