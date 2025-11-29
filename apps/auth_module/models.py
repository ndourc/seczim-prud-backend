from django.db import models
from django.contrib.auth.models import User
from apps.core.models import SMI

class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('ADMIN', 'Administrator'),
        ('PRINCIPAL_OFFICER', 'Principal Officer'),
        ('ACCOUNTANT', 'Accountant'),
        ('COMPLIANCE_OFFICER', 'Compliance Officer'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    smi = models.ForeignKey(SMI, on_delete=models.CASCADE, null=True, blank=True)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES)
    phone_number = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    department = models.CharField(max_length=100, blank=True)
    position = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.role}"

    class Meta:
        permissions = [
            ("can_view_smi_data", "Can view SMI data"),
            ("can_edit_smi_data", "Can edit SMI data"),
            ("can_view_reports", "Can view reports"),
            ("can_create_reports", "Can create reports"),
        ]
