from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ComplianceIndexViewSet, ComplianceAssessmentViewSet, ComplianceRequirementViewSet,
    ComplianceViolationViewSet, ComplianceReportViewSet
)

router = DefaultRouter()
router.register(r'compliance-indices', ComplianceIndexViewSet)
router.register(r'assessments', ComplianceAssessmentViewSet)
router.register(r'requirements', ComplianceRequirementViewSet)
router.register(r'violations', ComplianceViolationViewSet)
router.register(r'reports', ComplianceReportViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
