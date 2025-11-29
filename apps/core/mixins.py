from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count, Avg, Case, When, IntegerField
from django.utils import timezone
from datetime import timedelta

class RiskAssessmentSummaryMixin:
    @action(detail=False, methods=['get'])
    def summary_statistics(self, request):
        queryset = self.get_queryset()
        
        # Get total count
        total_assessments = queryset.count()
        
        # Get risk level distribution
        risk_distribution = queryset.aggregate(
            high_risk=Count(Case(When(risk_level='HIGH', then=1), output_field=IntegerField())),
            medium_risk=Count(Case(When(risk_level='MEDIUM', then=1), output_field=IntegerField())),
            low_risk=Count(Case(When(risk_level='LOW', then=1), output_field=IntegerField()))
        )
        
        # Get average compliance score
        avg_compliance = queryset.aggregate(avg_score=Avg('compliance_score'))['avg_score']
        
        # Get recent assessments (last 30 days)
        thirty_days_ago = timezone.now() - timedelta(days=30)
        recent_assessments = queryset.filter(created_at__gte=thirty_days_ago).count()
        
        # Get pending actions count
        pending_actions = queryset.filter(status='PENDING').count()
        
        return Response({
            'total_assessments': total_assessments,
            'risk_distribution': risk_distribution,
            'average_compliance_score': avg_compliance,
            'recent_assessments': recent_assessments,
            'pending_actions': pending_actions
        })
        
        risk_profile = {
            'highRisk': 0,
            'mediumRisk': 0,
            'lowRisk': 0
        }
        
        for item in risk_distribution:
            if item['risk_rating'] == 'HIGH':
                risk_profile['highRisk'] = item['count']
            elif item['risk_rating'] == 'MEDIUM':
                risk_profile['mediumRisk'] = item['count']
            elif item['risk_rating'] == 'LOW':
                risk_profile['lowRisk'] = item['count']
        
        # Calculate average FSI score
        avg_fsi = self.get_queryset().aggregate(Avg('fsi_score'))['fsi_score__avg'] or 0
        
        return Response({
            **risk_profile,
            'averageFSI': round(avg_fsi, 2),
            'totalAssessments': self.get_queryset().count(),
            'recentAssessments': self.get_recent_assessments()
        })
    
    def get_recent_assessments(self):
        thirty_days_ago = timezone.now() - timedelta(days=30)
        recent = (
            self.get_queryset()
            .filter(assessment_date__gte=thirty_days_ago)
            .order_by('-assessment_date')[:5]
        )
        
        return [
            {
                'id': assessment.id,
                'smiName': assessment.smi.company_name,
                'date': assessment.assessment_date,
                'riskRating': assessment.risk_rating,
                'fsiScore': assessment.fsi_score
            }
            for assessment in recent
        ]
