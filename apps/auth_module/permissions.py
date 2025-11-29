from rest_framework import permissions
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

class IsAdminUser(permissions.BasePermission):
    """
    Allow access only to admin users.
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_staff)

class IsPrincipalOfficer(permissions.BasePermission):
    """
    Allow access only to Principal Officers.
    """
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        try:
            profile = request.user.userprofile
            return profile.role == 'PRINCIPAL_OFFICER'
        except:
            return False

class IsAccountant(permissions.BasePermission):
    """
    Allow access only to Accountants.
    """
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        try:
            profile = request.user.userprofile
            return profile.role == 'ACCOUNTANT'
        except:
            return False

class IsComplianceOfficer(permissions.BasePermission):
    """
    Allow access only to Compliance Officers.
    """
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        try:
            profile = request.user.userprofile
            return profile.role == 'COMPLIANCE_OFFICER'
        except:
            return False

class CanViewSmiData(permissions.BasePermission):
    """
    Allow access to view SMI data for users with appropriate permissions.
    """
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        # Admin users can view everything
        if request.user.is_staff:
            return True
        
        try:
            profile = request.user.userprofile
            # All roles can view SMI data
            return profile.role in ['ADMIN', 'PRINCIPAL_OFFICER', 'ACCOUNTANT', 'COMPLIANCE_OFFICER']
        except:
            return False

class CanEditSmiData(permissions.BasePermission):
    """
    Allow access to edit SMI data for users with appropriate permissions.
    """
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        # Admin users can edit everything
        if request.user.is_staff:
            return True
        
        try:
            profile = request.user.userprofile
            # Only Accountants and Compliance Officers can edit SMI data
            return profile.role in ['ADMIN', 'ACCOUNTANT', 'COMPLIANCE_OFFICER']
        except:
            return False

class CanViewReports(permissions.BasePermission):
    """
    Allow access to view reports for users with appropriate permissions.
    """
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        # Admin users can view everything
        if request.user.is_staff:
            return True
        
        try:
            profile = request.user.userprofile
            # All roles can view reports
            return profile.role in ['ADMIN', 'PRINCIPAL_OFFICER', 'ACCOUNTANT', 'COMPLIANCE_OFFICER']
        except:
            return False

class CanCreateReports(permissions.BasePermission):
    """
    Allow access to create reports for users with appropriate permissions.
    """
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        # Admin users can create everything
        if request.user.is_staff:
            return True
        
        try:
            profile = request.user.userprofile
            # Only Compliance Officers and Accountants can create reports
            return profile.role in ['ADMIN', 'ACCOUNTANT', 'COMPLIANCE_OFFICER']
        except:
            return False

class CanManageCases(permissions.BasePermission):
    """
    Allow access to manage cases for users with appropriate permissions.
    """
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        # Admin users can manage everything
        if request.user.is_staff:
            return True
        
        try:
            profile = request.user.userprofile
            # Only Compliance Officers can manage cases
            return profile.role in ['ADMIN', 'COMPLIANCE_OFFICER']
        except:
            return False

class CanViewRiskAssessments(permissions.BasePermission):
    """
    Allow access to view risk assessments for users with appropriate permissions.
    """
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        # Admin users can view everything
        if request.user.is_staff:
            return True
        
        try:
            profile = request.user.userprofile
            # All roles can view risk assessments
            return profile.role in ['ADMIN', 'PRINCIPAL_OFFICER', 'ACCOUNTANT', 'COMPLIANCE_OFFICER']
        except:
            return False

class CanCreateRiskAssessments(permissions.BasePermission):
    """
    Allow access to create risk assessments for users with appropriate permissions.
    """
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        # Admin users can create everything
        if request.user.is_staff:
            return True
        
        try:
            profile = request.user.userprofile
            # Only Compliance Officers can create risk assessments
            return profile.role in ['ADMIN', 'COMPLIANCE_OFFICER']
        except:
            return False

class CanViewFinancialData(permissions.BasePermission):
    """
    Allow access to view financial data for users with appropriate permissions.
    """
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        # Admin users can view everything
        if request.user.is_staff:
            return True
        
        try:
            profile = request.user.userprofile
            # All roles can view financial data
            return profile.role in ['ADMIN', 'PRINCIPAL_OFFICER', 'ACCOUNTANT', 'COMPLIANCE_OFFICER']
        except:
            return False

class CanEditFinancialData(permissions.BasePermission):
    """
    Allow access to edit financial data for users with appropriate permissions.
    """
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        # Admin users can edit everything
        if request.user.is_staff:
            return True
        
        try:
            profile = request.user.userprofile
            # Only Accountants can edit financial data
            return profile.role in ['ADMIN', 'ACCOUNTANT']
        except:
            return False

class CanViewInspectionReports(permissions.BasePermission):
    """
    Allow access to view inspection reports for users with appropriate permissions.
    """
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        # Admin users can view everything
        if request.user.is_staff:
            return True
        
        try:
            profile = request.user.userprofile
            # All roles can view inspection reports
            return profile.role in ['ADMIN', 'PRINCIPAL_OFFICER', 'ACCOUNTANT', 'COMPLIANCE_OFFICER']
        except:
            return False

class CanCreateInspectionReports(permissions.BasePermission):
    """
    Allow access to create inspection reports for users with appropriate permissions.
    """
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        # Admin users can create everything
        if request.user.is_staff:
            return True
        
        try:
            profile = request.user.userprofile
            # Only Compliance Officers can create inspection reports
            return profile.role in ['ADMIN', 'COMPLIANCE_OFFICER']
        except:
            return False

class CanViewNotifications(permissions.BasePermission):
    """
    Allow access to view notifications for users with appropriate permissions.
    """
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        # All authenticated users can view their own notifications
        return True

class CanViewAuditLogs(permissions.BasePermission):
    """
    Allow access to view audit logs for users with appropriate permissions.
    """
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        # Only admin users can view audit logs
        return request.user.is_staff

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed for any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Instance must have an attribute named `owner`.
        return obj.user == request.user

class IsSmiOwnerOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow SMI owners to edit their data.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed for any request
        if request.method in permissions.SAFE_METHODS:
            return True

        # Check if user is associated with the SMI
        try:
            user_profile = request.user.userprofile
            if user_profile.smi == obj.smi:
                return True
        except:
            pass
        
        # Admin users can edit everything
        return request.user.is_staff

