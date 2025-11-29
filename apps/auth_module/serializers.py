from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile
from apps.core.serializers import SMISerializer

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_active', 'date_joined']
        read_only_fields = ['id', 'date_joined']

class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    smi = SMISerializer(read_only=True)
    smi_id = serializers.UUIDField(write_only=True, required=False)
    
    class Meta:
        model = UserProfile
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    confirm_password = serializers.CharField(write_only=True)
    role = serializers.ChoiceField(choices=UserProfile.ROLE_CHOICES, required=False)
    smi_id = serializers.UUIDField(required=False)
    phone_number = serializers.CharField(required=False, max_length=20)
    department = serializers.CharField(required=False, max_length=100)
    position = serializers.CharField(required=False, max_length=100)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'confirm_password', 'first_name', 'last_name', 
                 'role', 'smi_id', 'phone_number', 'department', 'position']
    
    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match")
        return data
    
    def create(self, validated_data):
        # Remove non-User fields
        validated_data.pop('role', None)
        validated_data.pop('smi_id', None)
        validated_data.pop('phone_number', None)
        validated_data.pop('department', None)
        validated_data.pop('position', None)
        validated_data.pop('confirm_password', None)
        
        user = User.objects.create_user(**validated_data)
        return user

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField()
    new_password = serializers.CharField(min_length=8)

class PasswordResetSerializer(serializers.Serializer):
    username = serializers.CharField()
    new_password = serializers.CharField(min_length=8)

class UserProfileUpdateSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = UserProfile
        fields = ['role', 'phone_number', 'smi', 'department', 'position']
        read_only_fields = ['id', 'created_at', 'updated_at']

class UserDashboardSerializer(serializers.ModelSerializer):
    """Dashboard serializer for user profile"""
    user = UserSerializer(read_only=True)
    smi = SMISerializer(read_only=True)
    
    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'role', 'smi', 'phone_number', 'department', 'position', 
                 'created_at', 'updated_at', 'last_login']

class UserManagementSerializer(serializers.ModelSerializer):
    """Serializer for admin user management"""
    user = UserSerializer(read_only=True)
    smi = SMISerializer(read_only=True)
    
    class Meta:
        model = UserProfile
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']

class UserSummarySerializer(serializers.ModelSerializer):
    """Summary serializer for user lists"""
    user = UserSerializer(read_only=True)
    smi_name = serializers.CharField(source='smi.name', read_only=True)
    
    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'role', 'smi_name', 'department', 'position', 'created_at']
