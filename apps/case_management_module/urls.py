from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CaseViewSet, CaseNoteViewSet, InvestigationViewSet, AdHocInspectionViewSet,
    CaseAttachmentViewSet, CaseTimelineViewSet
)

router = DefaultRouter()
router.register(r'cases', CaseViewSet)
router.register(r'case-notes', CaseNoteViewSet)
router.register(r'investigations', InvestigationViewSet)
router.register(r'ad-hoc-inspections', AdHocInspectionViewSet)
router.register(r'attachments', CaseAttachmentViewSet)
router.register(r'timeline', CaseTimelineViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

