from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from datetime import datetime, timedelta
import logging

from .models import (
    SMI, RiskAssessment, ComplianceIndex, Notification, 
    LicensingBreach, InspectionReport, Case
)

logger = logging.getLogger(__name__)

@shared_task
def calculate_risk_scores():
    """
    Calculate risk scores for all SMIs
    """
    try:
        smis = SMI.objects.filter(status='ACTIVE')
        for smi in smis:
            # Get latest financial data
            latest_financial = smi.financial_statements.order_by('-period').first()
            if not latest_financial:
                continue
            
            # Calculate FSI score based on financial ratios
            fsi_score = calculate_fsi_score(latest_financial)
            
            # Calculate Capital Adequacy Ratio
            car = calculate_car(latest_financial)
            
            # Determine risk level
            risk_level = determine_risk_level(fsi_score, car)
            
            # Create or update risk assessment
            risk_assessment, created = RiskAssessment.objects.get_or_create(
                smi=smi,
                assessment_date=timezone.now().date(),
                assessment_period='QUARTERLY',
                defaults={
                    'fsi_score': fsi_score,
                    'car': car,
                    'risk_level': risk_level,
                    'overall_risk_score': (fsi_score + (100 - car)) / 2,
                    'status': 'COMPLETED'
                }
            )
            
            if not created:
                risk_assessment.fsi_score = fsi_score
                risk_assessment.car = car
                risk_assessment.risk_level = risk_level
                risk_assessment.overall_risk_score = (fsi_score + (100 - car)) / 2
                risk_assessment.save()
        
        logger.info(f"Risk scores calculated for {smis.count()} SMIs")
        return True
        
    except Exception as e:
        logger.error(f"Error calculating risk scores: {str(e)}")
        return False

@shared_task
def send_pending_notifications():
    """
    Send pending notifications via email
    """
    try:
        pending_notifications = Notification.objects.filter(
            email_sent=False,
            created_at__gte=timezone.now() - timedelta(days=1)
        )
        
        for notification in pending_notifications:
            try:
                # Send email
                send_mail(
                    subject=notification.title,
                    message=notification.message,
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[notification.user.email],
                    fail_silently=False,
                )
                
                # Mark as sent
                notification.email_sent = True
                notification.email_sent_at = timezone.now()
                notification.save()
                
                logger.info(f"Notification sent to {notification.user.email}")
                
            except Exception as e:
                logger.error(f"Failed to send notification {notification.id}: {str(e)}")
        
        return True
        
    except Exception as e:
        logger.error(f"Error sending notifications: {str(e)}")
        return False

@shared_task
def update_compliance_indices():
    """
    Update compliance indices for all SMIs
    """
    try:
        smis = SMI.objects.filter(status='ACTIVE')
        current_period = timezone.now().date()
        
        for smi in smis:
            # Get latest risk assessment
            latest_risk = smi.risk_assessments.order_by('-assessment_date').first()
            if not latest_risk:
                continue
            
            # Get latest inspection reports
            latest_inspection = smi.inspection_reports.order_by('-inspection_date').first()
            
            # Calculate compliance score
            compliance_score = calculate_compliance_score(smi, latest_risk, latest_inspection)
            
            # Create or update compliance index
            compliance_index, created = ComplianceIndex.objects.get_or_create(
                smi=smi,
                period=current_period,
                analysis_period='QUARTERLY',
                defaults={
                    'overall_compliance_score': compliance_score,
                    'risk_calibration_score': compliance_score,
                    'final_compliance_score': compliance_score
                }
            )
            
            if not created:
                compliance_index.overall_compliance_score = compliance_score
                compliance_index.risk_calibration_score = compliance_score
                compliance_index.final_compliance_score = compliance_score
                compliance_index.save()
        
        logger.info(f"Compliance indices updated for {smis.count()} SMIs")
        return True
        
    except Exception as e:
        logger.error(f"Error updating compliance indices: {str(e)}")
        return False

@shared_task
def check_licensing_breaches():
    """
    Check for potential licensing breaches
    """
    try:
        smis = SMI.objects.filter(status='ACTIVE')
        
        for smi in smis:
            # Check for overdue inspections
            overdue_inspections = smi.inspection_reports.filter(
                status='OPEN',
                due_date__lt=timezone.now().date()
            )
            
            if overdue_inspections.exists():
                # Create breach record
                breach, created = LicensingBreach.objects.get_or_create(
                    smi=smi,
                    breach_type='MINOR',
                    breach_date=timezone.now().date(),
                    description='Overdue inspection report',
                    status='OPEN'
                )
                
                if created:
                    # Create notification
                    # user=smi.userprofile_set.first().user if smi.userprofile_set.exists() else None,  # Temporarily commented out
                    Notification.objects.create(
                        user=None,  # Temporarily set to None
                        notification_type='BREACH_ALERT',
                        title='Overdue Inspection Report',
                        message=f'Inspection report for {smi.company_name} is overdue',
                        priority='HIGH'
                    )
        
        logger.info("Licensing breaches checked")
        return True
        
    except Exception as e:
        logger.error(f"Error checking licensing breaches: {str(e)}")
        return False

@shared_task
def generate_risk_report():
    """
    Generate comprehensive risk report
    """
    try:
        # Get all active SMIs
        active_smis = SMI.objects.filter(status='ACTIVE')
        
        # Calculate industry averages
        industry_stats = {
            'total_smis': active_smis.count(),
            'high_risk_count': active_smis.filter(risk_assessments__risk_level='HIGH').distinct().count(),
            'medium_risk_count': active_smis.filter(risk_assessments__risk_level='MEDIUM').distinct().count(),
            'low_risk_count': active_smis.filter(risk_assessments__risk_level='LOW').distinct().count(),
        }
        
        # Generate report content
        report_content = f"""
        PRBS Risk Report - {timezone.now().strftime('%Y-%m-%d')}
        
        Industry Overview:
        - Total Active SMIs: {industry_stats['total_smis']}
        - High Risk: {industry_stats['high_risk_count']}
        - Medium Risk: {industry_stats['medium_risk_count']}
        - Low Risk: {industry_stats['low_risk_count']}
        
        Risk Distribution:
        - High Risk: {(industry_stats['high_risk_count']/industry_stats['total_smis']*100):.1f}%
        - Medium Risk: {(industry_stats['medium_risk_count']/industry_stats['total_smis']*100):.1f}%
        - Low Risk: {(industry_stats['low_risk_count']/industry_stats['total_smis']*100):.1f}%
        """
        
        # Create notification for compliance officers
        # compliance_users = UserProfile.objects.filter(role='COMPLIANCE_OFFICER')  # Temporarily commented out
        # for user_profile in compliance_users:
        #     Notification.objects.create(
        #         user=user_profile.user,
        #         notification_type='MARKET_SUBMISSION',
        #         title='Risk Report Generated',
        #         message=f'Monthly risk report has been generated. {industry_stats["high_risk_count"]} SMIs identified as high risk.',
        #         priority='MEDIUM'
        #     )
        
        logger.info("Risk report generated successfully")
        return True
        
    except Exception as e:
        logger.error(f"Error generating risk report: {str(e)}")
        return False

# Helper functions
def calculate_fsi_score(financial_statement):
    """
    Calculate Financial Stability Index score
    """
    try:
        # Simple scoring based on profitability and margins
        if financial_statement.profit_margin and financial_statement.profit_margin > 0:
            profit_score = min(100, financial_statement.profit_margin * 100)
        else:
            profit_score = 0
        
        if financial_statement.gross_margin and financial_statement.gross_margin > 0:
            margin_score = min(100, financial_statement.gross_margin * 100)
        else:
            margin_score = 0
        
        # Weighted average
        fsi_score = (profit_score * 0.6) + (margin_score * 0.4)
        return max(0, min(100, fsi_score))
        
    except Exception:
        return 50  # Default score

def calculate_car(financial_statement):
    """
    Calculate Capital Adequacy Ratio
    """
    try:
        if financial_statement.total_equity and financial_statement.total_assets:
            car = (financial_statement.total_equity / financial_statement.total_assets) * 100
            return max(0, min(100, car))
        return 50  # Default ratio
    except Exception:
        return 50

def determine_risk_level(fsi_score, car):
    """
    Determine risk level based on FSI score and CAR
    """
    if fsi_score >= 70 and car >= 15:
        return 'LOW'
    elif fsi_score >= 50 and car >= 10:
        return 'MEDIUM'
    else:
        return 'HIGH'

def calculate_compliance_score(smi, risk_assessment, inspection_report):
    """
    Calculate compliance score based on risk assessment and inspection results
    """
    base_score = 75  # Base compliance score
    
    # Adjust based on risk level
    if risk_assessment.risk_level == 'LOW':
        base_score += 15
    elif risk_assessment.risk_level == 'HIGH':
        base_score -= 20
    
    # Adjust based on inspection findings
    if inspection_report and inspection_report.status == 'RESOLVED':
        base_score += 10
    elif inspection_report and inspection_report.status == 'OPEN':
        base_score -= 15
    
    return max(0, min(100, base_score))

