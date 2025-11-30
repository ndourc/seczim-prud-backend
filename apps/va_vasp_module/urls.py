from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    VA_VASPViewSet, VirtualAssetViewSet, VASPServiceViewSet,
    VARiskAssessmentViewSet, VASPComplianceViewSet
)

router = DefaultRouter()
router.register(r'va-vasp', VA_VASPViewSet, basename='va-vasp')
router.register(r'virtual-assets', VirtualAssetViewSet)
router.register(r'vasp-services', VASPServiceViewSet)
router.register(r'risk-assessments', VARiskAssessmentViewSet)
router.register(r'compliance', VASPComplianceViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

