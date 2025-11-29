from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    LicensingPortalIntegrationViewSet, PortalSMIDataViewSet,
    InstitutionalProfileViewSet, ShareholderViewSet,
    DirectorViewSet, LicenseHistoryViewSet, LicensingPortalSyncViewSet
)

router = DefaultRouter()
router.register(r'portal-integration', LicensingPortalIntegrationViewSet)
router.register(r'portal-smi-data', PortalSMIDataViewSet)
router.register(r'institutional-profiles', InstitutionalProfileViewSet)
router.register(r'shareholders', ShareholderViewSet)
router.register(r'directors', DirectorViewSet)
router.register(r'license-history', LicenseHistoryViewSet)
router.register(r'sync', LicensingPortalSyncViewSet, basename='sync')

urlpatterns = [
    path('', include(router.urls)),
]

