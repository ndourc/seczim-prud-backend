from rest_framework import viewsets, status, permissions, serializers
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
    permission_classes = [permissions.AllowAny]  # TEMP: Auth disabled for testing
    
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
        # TESTING MODE: bypass role checks and create the assessment
        try:
            serializer.save(assessor=self.request.user)
            risk_assessment = serializer.instance
            risk_assessment.calculate_overall_risk_score()
            risk_assessment.determine_risk_level()
            risk_assessment.save()
        except Exception:
            serializer.save()
    
    def perform_update(self, serializer):
        # TESTING MODE: bypass role checks and update the assessment
        risk_assessment = serializer.save()
        try:
            risk_assessment.calculate_overall_risk_score()
            risk_assessment.determine_risk_level()
            risk_assessment.save()
        except Exception:
            pass
    
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
    permission_classes = [permissions.AllowAny]  # TEMP: Auth disabled for testing
    
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
    
    def perform_create(self, serializer):
        """Handle creating a new stress test"""
        # For industry-level tests, smi is optional
        smi_id = self.request.data.get('smi_id')
        test_type = self.request.data.get('test_type', 'SMI_LEVEL')
        
        if test_type != 'INDUSTRY_LEVEL' and smi_id:
            try:
                from apps.core.models import SMI
                smi = SMI.objects.get(id=smi_id)
                serializer.save(smi=smi)
            except SMI.DoesNotExist:
                raise serializers.ValidationError({'smi_id': 'Invalid SMI ID.'})
        else:
            serializer.save()
    
    def perform_update(self, serializer):
        """Handle updating a stress test"""
        smi_id = self.request.data.get('smi_id')
        test_type = self.request.data.get('test_type')
        
        if smi_id and test_type != 'INDUSTRY_LEVEL':
            try:
                from apps.core.models import SMI
                smi = SMI.objects.get(id=smi_id)
                serializer.save(smi=smi)
            except SMI.DoesNotExist:
                raise serializers.ValidationError({'smi_id': 'Invalid SMI ID.'})
        else:
            serializer.save()
    
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
    permission_classes = [permissions.AllowAny]  # TEMP: Auth disabled for testing
    
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
    
    def perform_create(self, serializer):
        """Handle creating a new risk indicator"""
        # Extract smi_id from request data
        smi_id = self.request.data.get('smi_id')
        
        if not smi_id:
            raise serializers.ValidationError({'smi_id': 'This field is required.'})
        
        try:
            # Get the SMI object
            from apps.core.models import SMI
            smi = SMI.objects.get(id=smi_id)
        except SMI.DoesNotExist:
            raise serializers.ValidationError({'smi_id': 'Invalid SMI ID.'})
        
        # Save with the resolved SMI object
        serializer.save(smi=smi)
    
    def perform_update(self, serializer):
        """Handle updating a risk indicator"""
        # Extract smi_id from request data if provided
        smi_id = self.request.data.get('smi_id')
        
        if smi_id:
            try:
                # Get the SMI object
                from apps.core.models import SMI
                smi = SMI.objects.get(id=smi_id)
                serializer.save(smi=smi)
            except SMI.DoesNotExist:
                raise serializers.ValidationError({'smi_id': 'Invalid SMI ID.'})
        else:
            # If smi_id not provided, keep existing smi
            serializer.save()
    
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
    permission_classes = [permissions.AllowAny]  # TEMP: Auth disabled for testing
    
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
    
    def perform_create(self, serializer):
        """Handle creating a new risk trend"""
        smi_id = self.request.data.get('smi_id')
        
        if not smi_id:
            raise serializers.ValidationError({'smi_id': 'This field is required.'})
        
        try:
            from apps.core.models import SMI
            smi = SMI.objects.get(id=smi_id)
        except SMI.DoesNotExist:
            raise serializers.ValidationError({'smi_id': 'Invalid SMI ID.'})
        
        serializer.save(smi=smi)
    
    def perform_update(self, serializer):
        """Handle updating a risk trend"""
        smi_id = self.request.data.get('smi_id')
        
        if smi_id:
            try:
                from apps.core.models import SMI
                smi = SMI.objects.get(id=smi_id)
                serializer.save(smi=smi)
            except SMI.DoesNotExist:
                raise serializers.ValidationError({'smi_id': 'Invalid SMI ID.'})
        else:
            serializer.save()
    
    @action(detail=False, methods=['get'])
    def trend_analysis(self, request):
        """Get risk trend analysis"""
        smi_id = request.query_params.get('smi_id')
        
        if smi_id:
            # Specific SMI analysis
            trends = self.get_queryset().filter(smi_id=smi_id).order_by('period_start')
            if not trends.exists():
                return Response({'error': 'No trend data found for this SMI'}, status=status.HTTP_404_NOT_FOUND)
            
            analysis = {
                'smi_id': smi_id,
                'smi_name': trends.first().smi.company_name if trends.first().smi else 'Unknown',
                'total_periods': trends.count(),
                'risk_trend': trends.last().risk_level_change,
                'financial_performance': trends.last().financial_performance,
                'compliance_performance': trends.last().compliance_performance,
                'trends': RiskTrendSerializer(trends, many=True).data
            }
            return Response(analysis)
        
        # Global analysis (list of all SMIs)
        results = []
        # Get all SMIs that have trends
        smi_ids = self.get_queryset().values_list('smi_id', flat=True).distinct()
        
        for s_id in smi_ids:
            trends = self.get_queryset().filter(smi_id=s_id).order_by('period_start')
            if trends.exists():
                latest = trends.last()
                results.append({
                    'smi_id': str(s_id),
                    'smi_name': latest.smi.company_name if latest.smi else 'Unknown',
                    'total_periods': trends.count(),
                    'risk_trend': latest.risk_level_change,
                    'financial_performance': latest.financial_performance,
                    'compliance_performance': latest.compliance_performance,
                    # For list view, maybe don't include full history to keep payload light
                    'latest_trend': RiskTrendSerializer(latest).data
                })
        
        return Response(results)
