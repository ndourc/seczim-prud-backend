from rest_framework import serializers
from django.utils import timezone
import re
from .models import (
    SMI, BoardMember, MeetingLog, ProductOffering, ClienteleProfile,
    FinancialStatement, ClientAssetMix, LicensingBreach, SupervisoryIntervention,
    Notification, SystemAuditLog, Committee, IncomeItem, Asset, Liability, 
    Debtor, Creditor, RelatedParty, CapitalPosition
)

class SMISerializer(serializers.ModelSerializer):
    class Meta:
        model = SMI
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']

class BoardMemberSerializer(serializers.ModelSerializer):
    smi = SMISerializer(read_only=True)
    smi_id = serializers.UUIDField(write_only=True)
    
    class Meta:
        model = BoardMember
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']

class MeetingLogSerializer(serializers.ModelSerializer):
    smi = SMISerializer(read_only=True)
    smi_id = serializers.UUIDField(write_only=True)
    
    class Meta:
        model = MeetingLog
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']

class ProductOfferingSerializer(serializers.ModelSerializer):
    smi = SMISerializer(read_only=True)
    smi_id = serializers.UUIDField(write_only=True)
    
    class Meta:
        model = ProductOffering
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']

class ClienteleProfileSerializer(serializers.ModelSerializer):
    smi = SMISerializer(read_only=True)
    smi_id = serializers.UUIDField(write_only=True)
    
    class Meta:
        model = ClienteleProfile
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']

class FinancialStatementSerializer(serializers.ModelSerializer):
    smi = SMISerializer(read_only=True)
    smi_id = serializers.UUIDField(write_only=True)
    
    class Meta:
        model = FinancialStatement
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']

class ClientAssetMixSerializer(serializers.ModelSerializer):
    smi = SMISerializer(read_only=True)
    smi_id = serializers.UUIDField(write_only=True)
    
    class Meta:
        model = ClientAssetMix
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']

class LicensingBreachSerializer(serializers.ModelSerializer):
    smi = SMISerializer(read_only=True)
    smi_id = serializers.UUIDField(write_only=True)
    assigned_to = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = LicensingBreach
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']

class SupervisoryInterventionSerializer(serializers.ModelSerializer):
    smi = SMISerializer(read_only=True)
    smi_id = serializers.UUIDField(write_only=True)
    
    class Meta:
        model = SupervisoryIntervention
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']

class NotificationSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = Notification
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']

class SystemAuditLogSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    ip_address = serializers.CharField(max_length=45)
    
    class Meta:
        model = SystemAuditLog
        fields = '__all__'
        read_only_fields = ['id', 'created_at']

class SMIDashboardSerializer(serializers.Serializer):
    """Dashboard serializer for SMI management"""
    total_smis = serializers.IntegerField()
    active_smis = serializers.IntegerField()
    suspended_smis = serializers.IntegerField()
    revoked_smis = serializers.IntegerField()
    recent_smis = SMISerializer(many=True)
    high_risk_smis = serializers.IntegerField()
    compliance_alerts = serializers.IntegerField()

class SMIDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer for SMI with related data"""
    board_members = BoardMemberSerializer(many=True, read_only=True)
    meeting_logs = MeetingLogSerializer(many=True, read_only=True)
    product_offerings = ProductOfferingSerializer(many=True, read_only=True)
    clientele_profiles = ClienteleProfileSerializer(many=True, read_only=True)
    financial_statements = FinancialStatementSerializer(many=True, read_only=True)
    client_asset_mixes = ClientAssetMixSerializer(many=True, read_only=True)
    licensing_breaches = LicensingBreachSerializer(many=True, read_only=True)
    supervisory_interventions = SupervisoryInterventionSerializer(many=True, read_only=True)
    
    class Meta:
        model = SMI
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']

class CommitteeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Committee
        fields = '__all__'
        read_only_fields = ['id', 'created_at']

class IncomeItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = IncomeItem
        fields = '__all__'
        read_only_fields = ['id']

class AssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asset
        fields = '__all__'
        read_only_fields = ['id']

class LiabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Liability
        fields = '__all__'
        read_only_fields = ['id']

class DebtorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Debtor
        fields = '__all__'
        read_only_fields = ['id']

class CreditorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Creditor
        fields = '__all__'
        read_only_fields = ['id']

class RelatedPartySerializer(serializers.ModelSerializer):
    class Meta:
        model = RelatedParty
        fields = '__all__'
        read_only_fields = ['id']

class CapitalPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CapitalPosition
        fields = '__all__'
        read_only_fields = ['id', 'created_at']

class OffsiteProfilingSerializer(serializers.Serializer):
    companyId = serializers.UUIDField()
    reportingPeriod = serializers.DictField()
    boardMembers = serializers.ListField(child=serializers.DictField())
    committees = serializers.ListField(child=serializers.DictField())
    products = serializers.ListField(child=serializers.DictField())
    clients = serializers.ListField(child=serializers.DictField())
    financialStatement = serializers.DictField()
    balanceSheet = serializers.DictField()
    clientAssets = serializers.ListField(child=serializers.DictField())
    capitalPosition = serializers.DictField()
    metadata = serializers.DictField(required=False)
    supportingDocuments = serializers.ListField(child=serializers.DictField(), required=False)

    def create(self, validated_data):
        smi_id = validated_data.get('companyId')
        reporting_period = validated_data.get('reportingPeriod') or {}
        # Normalize period end: accept 'end' or 'periodEnd' keys; default to today when missing/invalid
        raw_end = reporting_period.get('end') or reporting_period.get('periodEnd') or reporting_period.get('period')
        period_end = None
        if raw_end:
            if isinstance(raw_end, str):
                cleaned = raw_end.replace('“', '').replace('”', '').strip()
                if re.match(r'^\d{4}-\d{2}-\d{2}$', cleaned):
                    period_end = cleaned
            else:
                period_end = raw_end
        if not period_end:
            period_end = timezone.localdate()

        try:
            smi = SMI.objects.get(id=smi_id)
        except SMI.DoesNotExist:
            raise serializers.ValidationError("SMI not found")

        # 1. Board Members - Full replacement
        BoardMember.objects.filter(smi=smi).delete()
        for bm_data in validated_data.get('boardMembers', []):
            BoardMember.objects.create(
                smi=smi,
                name=bm_data.get('name'),
                position=bm_data.get('position'),
                appointment_date=bm_data.get('appointmentDate'),
            )

        # 2. Committees - Full replacement
        Committee.objects.filter(smi=smi).delete()
        for comm_data in validated_data.get('committees', []):
            Committee.objects.create(
                smi=smi,
                name=comm_data.get('name'),
                purpose=comm_data.get('purpose'),
                chairperson=comm_data.get('chairperson'),
                members=comm_data.get('members', []),
                meetings_held=comm_data.get('meetingsHeld'),
                meeting_frequency=comm_data.get('meetingFrequency')
            )

        # 3. Products - Full replacement
        ProductOffering.objects.filter(smi=smi).delete()
        for prod_data in validated_data.get('products', []):
            ProductOffering.objects.create(
                smi=smi,
                product_name=prod_data.get('productName'),
                product_category=prod_data.get('productType'),
                income_contribution=prod_data.get('concentrationPercentage')
            )

        # 4. Clients - Full replacement
        ClienteleProfile.objects.filter(smi=smi).delete()
        for client_data in validated_data.get('clients', []):
            client_type = client_data.get('clientType').upper()
            if client_type not in ['RETAIL', 'WHOLESALE', 'INSTITUTIONAL', 'CORPORATE']:
                client_type = 'RETAIL'

            ClienteleProfile.objects.create(
                smi=smi,
                client_type=client_type,
                client_count=0,
                income_contribution=client_data.get('concentrationPercentage'),
                period=period_end
            )

        # 5. Financial Statement (Income Statement) - Update or Create
        fs_data = validated_data.get('financialStatement')
        fs, created = FinancialStatement.objects.update_or_create(
            smi=smi,
            period=period_end,
            statement_type='COMPREHENSIVE_INCOME',
            defaults={
                'total_revenue': fs_data.get('totalRevenue'),
                'total_expenses': fs_data.get('operatingCosts'),
                'profit_before_tax': fs_data.get('profitBeforeTax'),
                'gross_margin': fs_data.get('grossMargin'),
                'profit_margin': fs_data.get('profitMargin')
            }
        )
        # Clear existing items for this statement
        IncomeItem.objects.filter(financial_statement=fs).delete()
        for item in fs_data.get('incomeItems', []):
            IncomeItem.objects.create(
                financial_statement=fs,
                category=item.get('category'),
                description=item.get('description'),
                amount=item.get('amount'),
                is_core=item.get('isCore')
            )

        # 6. Balance Sheet - Update or Create
        bs_data = validated_data.get('balanceSheet')
        bs, created = FinancialStatement.objects.update_or_create(
            smi=smi,
            period=period_end,
            statement_type='FINANCIAL_POSITION',
            defaults={
                'total_assets': bs_data.get('totalAssets'),
                'total_liabilities': bs_data.get('totalLiabilities'),
                'total_equity': bs_data.get('shareholdersFunds')
            }
        )
        
        # Clear existing details
        Asset.objects.filter(financial_statement=bs).delete()
        Liability.objects.filter(financial_statement=bs).delete()
        Debtor.objects.filter(financial_statement=bs).delete()
        Creditor.objects.filter(financial_statement=bs).delete()
        RelatedParty.objects.filter(financial_statement=bs).delete()

        for item in bs_data.get('assets', []):
            Asset.objects.create(
                financial_statement=bs,
                asset_type=item.get('assetType'),
                category=item.get('category'),
                value=item.get('value'),
                is_current=item.get('isCurrent'),
                acquisition_date=item.get('acquisitionDate')
            )
        for item in bs_data.get('liabilities', []):
            Liability.objects.create(
                financial_statement=bs,
                liability_type=item.get('liabilityType'),
                category=item.get('category'),
                value=item.get('value'),
                is_current=item.get('isCurrent'),
                due_date=item.get('dueDate')
            )
        for item in bs_data.get('debtors', []):
            Debtor.objects.create(
                financial_statement=bs,
                name=item.get('name'),
                amount=item.get('amount'),
                age_days=item.get('ageDays')
            )
        for item in bs_data.get('creditors', []):
            Creditor.objects.create(
                financial_statement=bs,
                name=item.get('name'),
                amount=item.get('amount'),
                due_date=item.get('dueDate')
            )
        for item in bs_data.get('relatedParties', []):
            RelatedParty.objects.create(
                financial_statement=bs,
                name=item.get('name'),
                relationship=item.get('relationship'),
                balance=item.get('balance'),
                transaction_type=item.get('type')
            )

        # 7. Client Assets - Replace for this period
        # Assuming period match
        ClientAssetMix.objects.filter(smi=smi, period=period_end).delete()
        for ca_data in validated_data.get('clientAssets', []):
            ClientAssetMix.objects.create(
                smi=smi,
                period=period_end,
                asset_class=ca_data.get('assetType'),
                allocation_percentage=ca_data.get('concentrationPercentage'),
                market_value=ca_data.get('value')
            )

        # 8. Capital Position - Update or Create
        cp_data = validated_data.get('capitalPosition')
        CapitalPosition.objects.update_or_create(
            smi=smi,
            calculation_date=cp_data.get('calculationDate'),
            defaults={
                'net_capital': cp_data.get('netCapital'),
                'required_capital': cp_data.get('requiredCapital'),
                'adjusted_liquid_capital': cp_data.get('adjustedLiquidCapital'),
                'is_compliant': cp_data.get('isCompliant'),
                'capital_adequacy_ratio': cp_data.get('capitalAdequacyRatio')
            }
        )

        # Update SMI status to ACTIVE if it was PENDING
        if smi.status == 'PENDING':
            smi.status = 'ACTIVE'
            smi.save()

        return validated_data