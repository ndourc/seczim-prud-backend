from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.utils.dateparse import parse_date
from django.db.models import Max
from apps.core.models import SMI
from apps.auth_module.models import UserProfile
from .models import SMISubmission
from .serializers import SMISubmissionSerializer, RiskAssessmentSerializer
from .risk_logic.services import calculate_risk_assessment


class SMISubmissionRBAC(permissions.BasePermission):
    """
    RBAC mapping:
    - SMI_DATA_ENTRY: ACCOUNTANT or COMPLIANCE_OFFICER -> POST/GET own company
    - SMI_VIEW_ONLY: PRINCIPAL_OFFICER -> GET own company only
    - COMMISSION_ANALYST: mapped to staff (is_staff) -> GET any company
    """

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        if request.method == 'POST':
            role = getattr(getattr(request.user, 'userprofile', None), 'role', None)
            return role in ['ACCOUNTANT', 'COMPLIANCE_OFFICER']
        # GET allowed for roles + staff
        if request.method in permissions.SAFE_METHODS:
            if request.user.is_staff:
                return True
            role = getattr(getattr(request.user, 'userprofile', None), 'role', None)
            return role in ['ACCOUNTANT', 'COMPLIANCE_OFFICER', 'PRINCIPAL_OFFICER']
        return False

    def has_object_permission(self, request, view, obj):
        # staff can view any
        if request.user.is_staff:
            return True
        user_smi = getattr(getattr(request.user, 'userprofile', None), 'smi', None)
        return user_smi and obj.smi_id == user_smi.id


class SMISubmissionView(APIView):
    permission_classes = [SMISubmissionRBAC]

    def get(self, request):
        """
        Retrieve the latest submission for a company. If staff, can specify companyId via query.
        Non-staff users are restricted to their own company.
        Optional query param: companyId
        """
        company_id = request.query_params.get('companyId')

        smi = None
        if request.user.is_staff and company_id:
            smi = SMI.objects.filter(license_number=company_id).first() or SMI.objects.filter(id=company_id).first()
        else:
            smi = getattr(getattr(request.user, 'userprofile', None), 'smi', None)

        if not smi:
            return Response({"detail": "Company not found or not permitted"}, status=status.HTTP_403_FORBIDDEN)

        latest = (
            SMISubmission.objects
            .filter(smi=smi)
            .order_by('-reporting_period__end')
            .first()
        )
        if not latest:
            return Response({"detail": "No submissions found"}, status=status.HTTP_404_NOT_FOUND)

        self.check_object_permissions(request, latest)
        data = SMISubmissionSerializer(latest).data
        return Response(data)

    def post(self, request):
        """
        Create a new submission. Only permitted roles for their own company.
        companyId in payload must match the user's company (unless staff, which we still disallow for POST by policy).
        """
        # Support multipart form where JSON is under 'data'
        incoming = request.data
        if isinstance(incoming, dict) and 'data' in incoming and isinstance(incoming['data'], str):
            import json
            try:
                incoming = json.loads(incoming['data'])
            except Exception:
                return Response({"detail": "Invalid JSON in 'data' field"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = SMISubmissionSerializer(data=incoming)
        serializer.is_valid(raise_exception=True)

        # Enforce ownership: companyId must be user's SMI
        company_id = serializer.validated_data.get('companyId')
        user_profile = getattr(request.user, 'userprofile', None)
        user_smi = getattr(user_profile, 'smi', None)

        target_smi = SMI.objects.filter(license_number=company_id).first() or SMI.objects.filter(id=company_id).first()
        if not target_smi:
            return Response({"companyId": ["Company not found"]}, status=status.HTTP_400_BAD_REQUEST)

        if not user_smi or user_smi.id != target_smi.id:
            return Response({"detail": "You can only submit for your own company"}, status=status.HTTP_403_FORBIDDEN)

        submission = serializer.save()
        return Response(SMISubmissionSerializer(submission).data, status=status.HTTP_201_CREATED)


class IsCommissionAnalyst(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        if request.user.is_staff:
            return True
        role = getattr(getattr(request.user, 'userprofile', None), 'role', None)
        return role == 'COMMISSION_ANALYST'


class CalculateRiskView(APIView):
    permission_classes = [IsCommissionAnalyst]

    def post(self, request, submission_id: int):
        try:
            ra = calculate_risk_assessment(submission_id)
        except SMISubmission.DoesNotExist:
            return Response({"detail": "Submission not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response(RiskAssessmentSerializer(ra).data, status=status.HTTP_200_OK)


