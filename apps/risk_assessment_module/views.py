from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db.models import Q, Avg, Max, Min
from datetime import datetime, timedelta

from .models import RiskAssessment, StressTest, RiskIndicator, RiskTrend
from .serializers import (
    RiskAssessmentSerializer, StressTestSerializer, RiskIndicatorSerializer,
    RiskTrendSerializer, RiskAssessmentSummarySerializer, StressTestSummarySerializer,
    RiskIndicatorAlertSerializer
)
from apps.core.models import SMI
from apps.auth_module.models import UserProfile

class RiskAssessmentViewSet(viewsets.ModelViewSet):
    """ViewSet for risk assessment management"""
    queryset = RiskAssessment.objects.all()
    serializer_class = RiskAssessmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by SMI if provided
        smi_id = self.request.query_params.get('smi_id')
        if smi_id:
            queryset = queryset.filter(smi_id=smi_id)
        
        # Filter by assessment period
        assessment_period = self.request.query_params.get('assessment_period')
        if assessment_period:
            queryset = queryset.filter(assessment_period=assessment_period)
        
        # Filter by risk level
        risk_level = self.request.query_params.get('risk_level')
        if risk_level:
            queryset = queryset.filter(risk_level=risk_level)
        
        # Filter by status
        status_filter = self.request.query_params.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        return queryset
    
    def perform_create(self, serializer):
        # Check if user has permission to create risk assessments
        user_profile = UserProfile.objects.get(user=self.request.user)
        if user_profile.role not in ['COMPLIANCE_OFFICER', 'ADMIN']:
            raise permissions.PermissionDenied("You don't have permission to create risk assessments")
        
        # Set the assessor
        serializer.save(assessor=self.request.user)
        
        # Calculate overall risk score and determine risk level
        risk_assessment = serializer.instance
        risk_assessment.calculate_overall_risk_score()
        risk_assessment.determine_risk_level()
        risk_assessment.save()
    
    def perform_update(self, serializer):
        # Check if user has permission to update risk assessments
        user_profile = UserProfile.objects.get(user=self.request.user)
        if user_profile.role not in ['COMPLIANCE_OFFICER', 'ADMIN']:
            raise permissions.PermissionDenied("You don't have permission to update risk assessments")
        
        # Save the instance
        risk_assessment = serializer.save()
        
        # Recalculate overall risk score and determine risk level
        risk_assessment.calculate_overall_risk_score()
        risk_assessment.determine_risk_level()
        risk_assessment.save()
    
    @action(detail=False, methods=['get'])
    def dashboard_summary(self, request):
        """Get risk assessment dashboard summary"""
        # Get recent assessments
        recent_assessments = self.get_queryset().order_by('-assessment_date')[:10]
        
        # Calculate statistics
        total_assessments = self.get_queryset().count()
        high_risk_count = self.get_queryset().filter(risk_level__in=['HIGH', 'CRITICAL']).count()
        pending_assessments = self.get_queryset().filter(status='PENDING').count()
        
        # Get average FSI score
        avg_fsi_score = self.get_queryset().aggregate(Avg('fsi_score'))['fsi_score__avg'] or 0
        
        summary_data = {
            'total_assessments': total_assessments,
            'high_risk_count': high_risk_count,
            'pending_assessments': pending_assessments,
            'average_fsi_score': round(avg_fsi_score, 2),
            'recent_assessments': RiskAssessmentSerializer(recent_assessments, many=True).data
        }
        
        return Response(summary_data)

    @action(detail=False, methods=['get'])
    def industry_ranking(self, request):
        """Return industry ranking across SMIs based on latest overall_risk_score and trend.

        Response structure:
        [
          {
            'smi_id': str,
            'smi_name': str,
            'overall_risk_score': float,
            'risk_level': str,
            'fsi_score': float,
            'trend': 'up' | 'down' | 'flat',
            'previous_overall_risk_score': float | None
          }, ...
        ] sorted by descending overall_risk_score (high risk first).
        """
        # Fetch the latest assessment per SMI
        latest_map = {}
        for ra in self.get_queryset().order_by('smi_id', '-assessment_date', '-created_at'):
            # keep only first seen (latest) per SMI
            if ra.smi_id not in latest_map:
                latest_map[ra.smi_id] = ra

        # Determine previous scores for trend
        ranking_rows = []
        for smi_id, latest in latest_map.items():
            previous = (
                self.get_queryset()
                .filter(smi_id=smi_id)
                .exclude(id=latest.id)
                .order_by('-assessment_date', '-created_at')
                .first()
            )
            prev_score = previous.overall_risk_score if previous else None
            if prev_score is None:
                trend = 'flat'
            else:
                if latest.overall_risk_score > prev_score:
                    trend = 'up'
                elif latest.overall_risk_score < prev_score:
                    trend = 'down'
                else:
                    trend = 'flat'

            ranking_rows.append({
                'smi_id': str(latest.smi_id),
                'smi_name': latest.smi.company_name,
                'overall_risk_score': round(latest.overall_risk_score, 2),
                'risk_level': latest.risk_level,
                'fsi_score': round(latest.fsi_score, 2),
                'trend': trend,
                'previous_overall_risk_score': round(prev_score, 2) if prev_score is not None else None,
            })

        # Sort by score descending (higher risk first) to mirror heat/risk chart ordering
        ranking_rows.sort(key=lambda r: r['overall_risk_score'], reverse=True)

        # Add ranking position
        for index, row in enumerate(ranking_rows, start=1):
            row['rank'] = index

        return Response(ranking_rows)
    
    @action(detail=True, methods=['post'])
    def recalculate_scores(self, request, pk=None):
        """Recalculate risk scores for an assessment"""
        risk_assessment = self.get_object()
        
        # Recalculate scores
        risk_assessment.calculate_overall_risk_score()
        risk_assessment.determine_risk_level()
        risk_assessment.save()
        
        return Response({
            'message': 'Risk scores recalculated successfully',
            'overall_risk_score': risk_assessment.overall_risk_score,
            'risk_level': risk_assessment.risk_level
        })

class StressTestViewSet(viewsets.ModelViewSet):
    """ViewSet for stress testing management"""
    queryset = StressTest.objects.all()
    serializer_class = StressTestSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by SMI if provided
        smi_id = self.request.query_params.get('smi_id')
        if smi_id:
            queryset = queryset.filter(smi_id=smi_id)
        
        # Filter by test type
        test_type = self.request.query_params.get('test_type')
        if test_type:
            queryset = queryset.filter(test_type=test_type)
        
        # Filter by pass/fail status
        passed = self.request.query_params.get('passed')
        if passed is not None:
            passed_bool = passed.lower() == 'true'
            queryset = queryset.filter(passed=passed_bool)
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def dashboard_summary(self, request):
        """Get stress testing dashboard summary"""
        # Get recent tests
        recent_tests = self.get_queryset().order_by('-test_date')[:10]
        
        # Calculate statistics
        total_tests = self.get_queryset().count()
        passed_tests = self.get_queryset().filter(passed=True).count()
        failed_tests = self.get_queryset().filter(passed=False).count()
        
        # Get latest test date
        latest_test = self.get_queryset().order_by('-test_date').first()
        last_test_date = latest_test.test_date if latest_test else None
        
        summary_data = {
            'total_tests': total_tests,
            'passed_tests': passed_tests,
            'failed_tests': failed_tests,
            'last_test_date': last_test_date,
            'recent_tests': StressTestSerializer(recent_tests, many=True).data
        }
        
        return Response(summary_data)

class RiskIndicatorViewSet(viewsets.ModelViewSet):
    """ViewSet for risk indicator management"""
    queryset = RiskIndicator.objects.all()
    serializer_class = RiskIndicatorSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by SMI if provided
        smi_id = self.request.query_params.get('smi_id')
        if smi_id:
            queryset = queryset.filter(smi_id=smi_id)
        
        # Filter by indicator type
        indicator_type = self.request.query_params.get('indicator_type')
        if indicator_type:
            queryset = queryset.filter(indicator_type=indicator_type)
        
        # Filter by breach status
        is_breached = self.request.query_params.get('is_breached')
        if is_breached is not None:
            is_breached_bool = is_breached.lower() == 'true'
            queryset = queryset.filter(is_breached=is_breached_bool)
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def alerts(self, request):
        """Get risk indicator alerts"""
        # Get breached indicators
        breached_indicators = self.get_queryset().filter(is_breached=True)
        
        alerts = []
        for indicator in breached_indicators:
            alert = {
                'indicator_name': indicator.indicator_name,
                'current_value': indicator.current_value,
                'threshold_value': indicator.threshold_value,
                'breach_level': indicator.alert_level,
                'smi_name': indicator.smi.company_name,
                'alert_message': f"{indicator.indicator_name} has breached threshold. Current: {indicator.current_value}, Threshold: {indicator.threshold_value}"
            }
            alerts.append(alert)
        
        return Response(alerts)

class RiskTrendViewSet(viewsets.ModelViewSet):
    """ViewSet for risk trend management"""
    queryset = RiskTrend.objects.all()
    serializer_class = RiskTrendSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by SMI if provided
        smi_id = self.request.query_params.get('smi_id')
        if smi_id:
            queryset = queryset.filter(smi_id=smi_id)
        
        # Filter by period
        period_start = self.request.query_params.get('period_start')
        if period_start:
            try:
                start_date = datetime.strptime(period_start, '%Y-%m-%d').date()
                queryset = queryset.filter(period_start__gte=start_date)
            except ValueError:
                pass
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def trend_analysis(self, request):
        """Get risk trend analysis"""
        smi_id = request.query_params.get('smi_id')
        if not smi_id:
            return Response({'error': 'SMI ID is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Get trends for the SMI
        trends = self.get_queryset().filter(smi_id=smi_id).order_by('period_start')
        
        if not trends.exists():
            return Response({'error': 'No trend data found for this SMI'}, status=status.HTTP_404_NOT_FOUND)
        
        # Analyze trends
        trend_analysis = {
            'smi_id': smi_id,
            'total_periods': trends.count(),
            'risk_trend': trends.last().risk_level_change if trends.exists() else 'STABLE',
            'financial_performance': trends.last().financial_performance if trends.exists() else 'NEUTRAL',
            'compliance_performance': trends.last().compliance_performance if trends.exists() else 'NEUTRAL',
            'trends': RiskTrendSerializer(trends, many=True).data
        }
        
        return Response(trend_analysis)
