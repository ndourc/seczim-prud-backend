from django.urls import path
from .views import SMISubmissionView, CalculateRiskView

urlpatterns = [
    path('smi-submission/', SMISubmissionView.as_view(), name='smi-submission'),
    path('submissions/<int:submission_id>/calculate-risk/', CalculateRiskView.as_view(), name='calculate-risk'),
]


