from rest_framework import serializers
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

    def create(self, validated_data):
        smi_id = validated_data.get('companyId')
        reporting_period = validated_data.get('reportingPeriod')
        period_end = reporting_period.get('end')

        try:
            smi = SMI.objects.get(id=smi_id)
        except SMI.DoesNotExist:
            raise serializers.ValidationError("SMI not found")

        # 1. Board Members
        for bm_data in validated_data.get('boardMembers', []):
            BoardMember.objects.create(
                smi=smi,
                name=bm_data.get('name'),
                position=bm_data.get('position'),
                appointment_date=bm_data.get('appointmentDate'),
                # map other fields if they exist in model, currently model has limited fields
            )

        # 2. Committees
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

        # 3. Products
        for prod_data in validated_data.get('products', []):
            ProductOffering.objects.create(
                smi=smi,
                product_name=prod_data.get('productName'),
                product_category=prod_data.get('productType'),
                income_contribution=prod_data.get('concentrationPercentage') # Mapping concentration to income contribution %
            )

        # 4. Clients
        for client_data in validated_data.get('clients', []):
            # Map frontend clientType to backend choices if needed
            client_type = client_data.get('clientType').upper()
            if client_type not in ['RETAIL', 'WHOLESALE', 'INSTITUTIONAL', 'CORPORATE']:
                client_type = 'RETAIL' # Default or handle error

            ClienteleProfile.objects.create(
                smi=smi,
                client_type=client_type,
                client_count=0, # Frontend doesn't send count, maybe default to 0 or infer?
                income_contribution=client_data.get('concentrationPercentage'),
                period=period_end
            )

        # 5. Financial Statement (Income Statement)
        fs_data = validated_data.get('financialStatement')
        fs = FinancialStatement.objects.create(
            smi=smi,
            period=period_end,
            statement_type='COMPREHENSIVE_INCOME',
            total_revenue=fs_data.get('totalRevenue'),
            total_expenses=fs_data.get('operatingCosts'),
            profit_before_tax=fs_data.get('profitBeforeTax'),
            gross_margin=fs_data.get('grossMargin'),
            profit_margin=fs_data.get('profitMargin')
        )
        for item in fs_data.get('incomeItems', []):
            IncomeItem.objects.create(
                financial_statement=fs,
                category=item.get('category'),
                description=item.get('description'),
                amount=item.get('amount'),
                is_core=item.get('isCore')
            )

        # 6. Balance Sheet
        bs_data = validated_data.get('balanceSheet')
        bs = FinancialStatement.objects.create(
            smi=smi,
            period=period_end,
            statement_type='FINANCIAL_POSITION',
            total_assets=bs_data.get('totalAssets'),
            total_liabilities=bs_data.get('totalLiabilities'),
            total_equity=bs_data.get('shareholdersFunds')
        )
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

        # 7. Client Assets
        for ca_data in validated_data.get('clientAssets', []):
            ClientAssetMix.objects.create(
                smi=smi,
                period=period_end,
                asset_class=ca_data.get('assetType'), # Needs mapping to choices?
                allocation_percentage=ca_data.get('concentrationPercentage'),
                market_value=ca_data.get('value')
            )

        # 8. Capital Position
        cp_data = validated_data.get('capitalPosition')
        CapitalPosition.objects.create(
            smi=smi,
            calculation_date=cp_data.get('calculationDate'),
            net_capital=cp_data.get('netCapital'),
            required_capital=cp_data.get('requiredCapital'),
            adjusted_liquid_capital=cp_data.get('adjustedLiquidCapital'),
            is_compliant=cp_data.get('isCompliant'),
            capital_adequacy_ratio=cp_data.get('capitalAdequacyRatio')
        )

        # Update SMI status to ACTIVE if it was PENDING
        if smi.status == 'PENDING':
            smi.status = 'ACTIVE'
            smi.save()

        return validated_data