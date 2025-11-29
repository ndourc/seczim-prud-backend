from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.db import transaction
from django.shortcuts import get_object_or_404
import logging

from .models import UserProfile
from .serializers import (
    UserSerializer, UserProfileSerializer, UserRegistrationSerializer,
    UserLoginSerializer, PasswordChangeSerializer, PasswordResetSerializer,
    UserDashboardSerializer
)
from apps.core.models import SMI

logger = logging.getLogger(__name__)

class AuthViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action in ['create', 'register', 'login']:
            return [permissions.AllowAny()]
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action == 'register':
            return UserRegistrationSerializer
        elif self.action == 'login':
            return UserLoginSerializer
        elif self.action == 'change_password':
            return PasswordChangeSerializer
        elif self.action == 'reset_password':
            return PasswordResetSerializer
        return UserSerializer

    @action(detail=False, methods=['post'])
    def register(self, request):
        """Register a new user with role-based profile"""
        try:
            with transaction.atomic():
                serializer = self.get_serializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                
                # Create user
                user = serializer.save()
                
                # Create user profile with role
                role = request.data.get('role', 'ACCOUNTANT')
                smi_id = request.data.get('smi_id')
                
                if smi_id:
                    try:
                        smi = SMI.objects.get(id=smi_id)
                    except SMI.DoesNotExist:
                        return Response(
                            {'error': 'Invalid SMI ID provided'},
                            status=status.HTTP_400_BAD_REQUEST
                        )
                else:
                    smi = None
                
                UserProfile.objects.create(
                    user=user,
                    role=role,
                    smi=smi,
                    phone_number=request.data.get('phone_number', ''),
                    department=request.data.get('department', ''),
                    position=request.data.get('position', '')
                )
                
                # Generate tokens
                refresh = RefreshToken.for_user(user)
                
                logger.info(f"New user registered: {user.username} with role: {role}")
                
                return Response({
                    'message': 'User registered successfully',
                    'user': UserSerializer(user).data,
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }, status=status.HTTP_201_CREATED)
                
        except Exception as e:
            logger.error(f"User registration failed: {str(e)}")
            return Response(
                {'error': 'Registration failed. Please try again.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=['post'])
    def login(self, request):
        """Authenticate user and return tokens"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        
        user = authenticate(username=username, password=password)
        
        if user is not None:
            if user.is_active:
                login(request, user)
                
                # Generate tokens
                refresh = RefreshToken.for_user(user)
                
                # Get user profile
                try:
                    profile = UserProfile.objects.get(user=user)
                    profile.last_login = timezone.now()
                    profile.save()
                except UserProfile.DoesNotExist:
                    pass
                
                logger.info(f"User logged in: {username}")
                
                return Response({
                    'message': 'Login successful',
                    'user': UserSerializer(user).data,
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                })
            else:
                return Response(
                    {'error': 'Account is disabled'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            return Response(
                {'error': 'Invalid credentials'},
                status=status.HTTP_401_UNAUTHORIZED
            )

    @action(detail=False, methods=['post'])
    def logout(self, request):
        """Logout user and invalidate tokens"""
        try:
            logout(request)
            logger.info(f"User logged out: {request.user.username}")
            return Response({'message': 'Logout successful'})
        except Exception as e:
            logger.error(f"Logout failed: {str(e)}")
            return Response(
                {'error': 'Logout failed'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=['post'])
    def change_password(self, request):
        """Change user password"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = request.user
        old_password = serializer.validated_data['old_password']
        new_password = serializer.validated_data['new_password']
        
        if not user.check_password(old_password):
            return Response(
                {'error': 'Current password is incorrect'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            validate_password(new_password, user)
            user.set_password(new_password)
            user.save()
            
            logger.info(f"Password changed for user: {user.username}")
            return Response({'message': 'Password changed successfully'})
            
        except ValidationError as e:
            return Response(
                {'error': 'Password validation failed', 'details': e.messages},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=False, methods=['post'])
    def reset_password(self, request):
        """Reset user password (admin only)"""
        if not request.user.is_staff:
            return Response(
                {'error': 'Permission denied'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        username = serializer.validated_data['username']
        new_password = serializer.validated_data['new_password']
        
        try:
            user = User.objects.get(username=username)
            user.set_password(new_password)
            user.save()
            
            logger.info(f"Password reset for user: {username} by admin: {request.user.username}")
            return Response({'message': 'Password reset successfully'})
            
        except User.DoesNotExist:
            return Response(
                {'error': 'User not found'},
                status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=False)
    def me(self, request):
        """Get current user information"""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @action(detail=False)
    def dashboard(self, request):
        """Get user dashboard data"""
        try:
            profile = UserProfile.objects.get(user=request.user)
            serializer = UserDashboardSerializer(profile)
            return Response(serializer.data)
        except UserProfile.DoesNotExist:
            return Response(
                {'error': 'User profile not found'},
                status=status.HTTP_404_NOT_FOUND
            )

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAdminUser()]
        return super().get_permissions()

    def get_queryset(self):
        if self.request.user.is_staff:
            return self.queryset
        return self.queryset.filter(id=self.request.user.id)

    @action(detail=True, methods=['post'])
    def activate(self, request, pk=None):
        """Activate/deactivate user account (admin only)"""
        if not request.user.is_staff:
            return Response(
                {'error': 'Permission denied'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        user = self.get_object()
        user.is_active = not user.is_active
        user.save()
        
        status_text = 'activated' if user.is_active else 'deactivated'
        logger.info(f"User {user.username} {status_text} by admin: {request.user.username}")
        
        return Response({
            'message': f'User {status_text} successfully',
            'is_active': user.is_active
        })

    @action(detail=True, methods=['post'])
    def make_staff(self, request, pk=None):
        """Grant/revoke staff privileges (admin only)"""
        if not request.user.is_staff:
            return Response(
                {'error': 'Permission denied'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        user = self.get_object()
        user.is_staff = not user.is_staff
        user.save()
        
        status_text = 'granted' if user.is_staff else 'revoked'
        logger.info(f"Staff privileges {status_text} for user {user.username} by admin: {request.user.username}")
        
        return Response({
            'message': f'Staff privileges {status_text} successfully',
            'is_staff': user.is_staff
        })

class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return self.queryset
        return self.queryset.filter(user=self.request.user)

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            # Allow users to update their own profile
            if self.action in ['update', 'partial_update']:
                return [permissions.IsAuthenticated()]
            return [permissions.IsAdminUser()]
        return super().get_permissions()

    def perform_update(self, serializer):
        """Ensure users can only update their own profile unless admin"""
        if not self.request.user.is_staff:
            profile = serializer.instance
            if profile.user != self.request.user:
                raise permissions.PermissionDenied("You can only update your own profile")
        serializer.save()

    @action(detail=False)
    def by_role(self, request):
        """Get users by role (admin only)"""
        if not request.user.is_staff:
            return Response(
                {'error': 'Permission denied'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        role = request.query_params.get('role')
        if not role:
            return Response(
                {'error': 'Role parameter is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        profiles = self.queryset.filter(role=role)
        serializer = self.get_serializer(profiles, many=True)
        return Response(serializer.data)

    @action(detail=False)
    def by_smi(self, request):
        """Get users by SMI (admin only)"""
        if not request.user.is_staff:
            return Response(
                {'error': 'Permission denied'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        smi_id = request.query_params.get('smi_id')
        if not smi_id:
            return Response(
                {'error': 'SMI ID parameter is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            smi = SMI.objects.get(id=smi_id)
            profiles = self.queryset.filter(smi=smi)
            serializer = self.get_serializer(profiles, many=True)
            return Response(serializer.data)
        except SMI.DoesNotExist:
            return Response(
                {'error': 'SMI not found'},
                status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=True, methods=['post'])
    def change_role(self, request, pk=None):
        """Change user role (admin only)"""
        if not request.user.is_staff:
            return Response(
                {'error': 'Permission denied'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        profile = self.get_object()
        new_role = request.data.get('role')
        
        if not new_role or new_role not in dict(UserProfile.ROLE_CHOICES):
            return Response(
                {'error': 'Valid role is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        old_role = profile.role
        profile.role = new_role
        profile.save()
        
        logger.info(f"Role changed for user {profile.user.username}: {old_role} -> {new_role} by admin: {request.user.username}")
        
        return Response({
            'message': 'Role changed successfully',
            'old_role': old_role,
            'new_role': new_role
        })
