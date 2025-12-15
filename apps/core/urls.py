from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    SMIViewSet, BoardMemberViewSet, MeetingLogViewSet, ProductOfferingViewSet,
    ClienteleProfileViewSet, FinancialStatementViewSet, ClientAssetMixViewSet,
    LicensingBreachViewSet, SupervisoryInterventionViewSet,
    NotificationViewSet, SystemAuditLogViewSet, OffsiteProfilingViewSet
)
from .formula_views import CalculationFormulaViewSet, CalculationBreakdownViewSet

router = DefaultRouter()
router.register(r'smis', SMIViewSet)
router.register(r'board-members', BoardMemberViewSet)
router.register(r'meeting-logs', MeetingLogViewSet)
router.register(r'product-offerings', ProductOfferingViewSet)
router.register(r'clientele-profiles', ClienteleProfileViewSet)
router.register(r'financial-statements', FinancialStatementViewSet)
router.register(r'client-asset-mixes', ClientAssetMixViewSet)

router.register(r'licensing-breaches', LicensingBreachViewSet)
router.register(r'supervisory-interventions', SupervisoryInterventionViewSet)

router.register(r'notifications', NotificationViewSet)
router.register(r'audit-logs', SystemAuditLogViewSet)
router.register(r'offsite-profiling', OffsiteProfilingViewSet, basename='offsite-profiling')

# Formula management endpoints
router.register(r'calculation-formulae', CalculationFormulaViewSet, basename='calculation-formula')
router.register(r'calculation-breakdowns', CalculationBreakdownViewSet, basename='calculation-breakdown')

urlpatterns = [
    path('', include(router.urls)),
]