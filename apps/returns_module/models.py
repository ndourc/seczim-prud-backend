from django.db import models
from apps.core.models import SMI

class PrudentialReturn(models.Model):
    STATUS_CHOICES = [
        ('DRAFT', 'Draft'),
        ('SUBMITTED', 'Submitted'),
        ('UNDER_REVIEW', 'Under Review'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    ]

    smi = models.ForeignKey(SMI, on_delete=models.CASCADE)
    reporting_period = models.DateField()
    submission_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.smi.company_name} - {self.reporting_period}"

class IncomeStatement(models.Model):
    prudential_return = models.OneToOneField(PrudentialReturn, on_delete=models.CASCADE)
    revenue = models.DecimalField(max_digits=15, decimal_places=2)
    operating_expenses = models.DecimalField(max_digits=15, decimal_places=2)
    net_profit = models.DecimalField(max_digits=15, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.prudential_return.smi.company_name} - {self.prudential_return.reporting_period}"

class BalanceSheet(models.Model):
    prudential_return = models.OneToOneField(PrudentialReturn, on_delete=models.CASCADE)
    total_assets = models.DecimalField(max_digits=15, decimal_places=2)
    total_liabilities = models.DecimalField(max_digits=15, decimal_places=2)
    equity = models.DecimalField(max_digits=15, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.prudential_return.smi.company_name} - {self.prudential_return.reporting_period}"
