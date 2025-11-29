from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    RiskAssessmentViewSet, StressTestViewSet, RiskIndicatorViewSet, RiskTrendViewSet
)

router = DefaultRouter()
router.register(r'assessments', RiskAssessmentViewSet)
router.register(r'stress-tests', StressTestViewSet)
router.register(r'indicators', RiskIndicatorViewSet)
router.register(r'trends', RiskTrendViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

