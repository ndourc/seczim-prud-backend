from rest_framework import serializers
from apps.core.models import SMI
from .models import (
    ReportingPeriod,
    SMISubmission,
    RiskAssessment,
    BoardMember,
    Committee,
    Product,
    Client,
    FinancialStatement,
    IncomeItem,
    BalanceSheet,
    BalanceAsset,
    BalanceLiability,
    Debtor,
    Creditor,
    RelatedParty,
    ClientAsset,
    CapitalPosition,
    SubmissionMetadata,
)
class RiskAssessmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = RiskAssessment
        fields = [
            "credit_risk_weight","credit_risk_score","credit_risk_rating",
            "market_risk_weight","market_risk_score","market_risk_rating",
            "liquidity_risk_weight","liquidity_risk_score","liquidity_risk_rating",
            "operational_risk_weight","operational_risk_score","operational_risk_rating",
            "legal_risk_weight","legal_risk_score","legal_risk_rating",
            "compliance_risk_weight","compliance_risk_score","compliance_risk_rating",
            "strategic_risk_weight","strategic_risk_score","strategic_risk_rating",
            "reputation_risk_weight","reputation_risk_score","reputation_risk_rating",
            "composite_risk_rating","fsi_score",
        ]



class ReportingPeriodSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportingPeriod
        fields = ["start", "end"]


class BoardMemberSerializer(serializers.ModelSerializer):
    appointmentDate = serializers.DateField(source="appointment_date")
    isPEP = serializers.BooleanField(source="is_pep")
    id = serializers.CharField(source="frontend_id", required=False, allow_blank=True)

    class Meta:
        model = BoardMember
        fields = [
            "name",
            "position",
            "appointmentDate",
            "qualifications",
            "experience",
            "isPEP",
            "id",
        ]


class CommitteeSerializer(serializers.ModelSerializer):
    meetingsHeld = serializers.IntegerField(source="meetings_held")
    meetingFrequency = serializers.CharField(source="meeting_frequency")
    id = serializers.CharField(source="frontend_id", required=False, allow_blank=True)

    class Meta:
        model = Committee
        fields = [
            "name",
            "purpose",
            "chairperson",
            "members",
            "meetingsHeld",
            "meetingFrequency",
            "id",
        ]


class ProductSerializer(serializers.ModelSerializer):
    productName = serializers.CharField(source="product_name")
    productType = serializers.CharField(source="product_type")
    launchDate = serializers.DateField(source="launch_date", allow_null=True, required=False)
    concentrationPercentage = serializers.DecimalField(source="concentration_percentage", max_digits=5, decimal_places=2, required=False, allow_null=True)
    id = serializers.CharField(source="frontend_id", required=False, allow_blank=True)

    class Meta:
        model = Product
        fields = [
            "productName",
            "productType",
            "launchDate",
            "income",
            "id",
            "concentrationPercentage",
        ]


class ClientSerializer(serializers.ModelSerializer):
    clientName = serializers.CharField(source="client_name")
    clientType = serializers.CharField(source="client_type")
    onboardingDate = serializers.DateField(source="onboarding_date", allow_null=True, required=False)
    concentrationPercentage = serializers.DecimalField(source="concentration_percentage", max_digits=5, decimal_places=2, required=False, allow_null=True)
    id = serializers.CharField(source="frontend_id", required=False, allow_blank=True)

    class Meta:
        model = Client
        fields = [
            "clientName",
            "clientType",
            "onboardingDate",
            "income",
            "id",
            "concentrationPercentage",
        ]


class IncomeItemSerializer(serializers.ModelSerializer):
    isCore = serializers.BooleanField(source="is_core")
    id = serializers.CharField(source="frontend_id", required=False, allow_blank=True)

    class Meta:
        model = IncomeItem
        fields = ["category", "description", "amount", "isCore", "id"]


class FinancialStatementSerializer(serializers.ModelSerializer):
    periodStart = serializers.DateField(source="period_start")
    periodEnd = serializers.DateField(source="period_end")
    totalRevenue = serializers.DecimalField(source="total_revenue", max_digits=18, decimal_places=2)
    operatingCosts = serializers.DecimalField(source="operating_costs", max_digits=18, decimal_places=2)
    profitBeforeTax = serializers.DecimalField(source="profit_before_tax", max_digits=18, decimal_places=2)
    grossMargin = serializers.DecimalField(source="gross_margin", max_digits=7, decimal_places=2, required=False, allow_null=True)
    profitMargin = serializers.DecimalField(source="profit_margin", max_digits=7, decimal_places=2, required=False, allow_null=True)
    incomeItems = IncomeItemSerializer(many=True, source="income_items")

    class Meta:
        model = FinancialStatement
        fields = [
            "periodStart",
            "periodEnd",
            "totalRevenue",
            "operatingCosts",
            "profitBeforeTax",
            "grossMargin",
            "profitMargin",
            "incomeItems",
        ]

    def create(self, validated_data):
        items = validated_data.pop("income_items", [])
        instance = FinancialStatement.objects.create(**validated_data)
        for item in items:
            IncomeItem.objects.create(financial_statement=instance, **item)
        return instance

    def update(self, instance, validated_data):
        items = validated_data.pop("income_items", None)
        for attr, val in validated_data.items():
            setattr(instance, attr, val)
        instance.save()
        if items is not None:
            instance.income_items.all().delete()
            for item in items:
                IncomeItem.objects.create(financial_statement=instance, **item)
        return instance


class BalanceAssetSerializer(serializers.ModelSerializer):
    assetType = serializers.CharField(source="asset_type")
    isCurrent = serializers.BooleanField(source="is_current")
    acquisitionDate = serializers.DateField(source="acquisition_date", allow_null=True, required=False)
    id = serializers.CharField(source="frontend_id", required=False, allow_blank=True)

    class Meta:
        model = BalanceAsset
        fields = [
            "assetType",
            "category",
            "value",
            "isCurrent",
            "acquisitionDate",
            "id",
        ]


class BalanceLiabilitySerializer(serializers.ModelSerializer):
    liabilityType = serializers.CharField(source="liability_type")
    isCurrent = serializers.BooleanField(source="is_current")
    dueDate = serializers.DateField(source="due_date", allow_null=True, required=False)
    id = serializers.CharField(source="frontend_id", required=False, allow_blank=True)

    class Meta:
        model = BalanceLiability
        fields = [
            "liabilityType",
            "category",
            "value",
            "isCurrent",
            "dueDate",
            "id",
        ]


class DebtorSerializer(serializers.ModelSerializer):
    ageDays = serializers.IntegerField(source="age_days")
    id = serializers.CharField(source="frontend_id", required=False, allow_blank=True)

    class Meta:
        model = Debtor
        fields = ["name", "amount", "ageDays", "id"]


class CreditorSerializer(serializers.ModelSerializer):
    dueDate = serializers.DateField(source="due_date", allow_null=True, required=False)
    id = serializers.CharField(source="frontend_id", required=False, allow_blank=True)

    class Meta:
        model = Creditor
        fields = ["name", "amount", "dueDate", "id"]


class RelatedPartySerializer(serializers.ModelSerializer):
    id = serializers.CharField(source="frontend_id", required=False, allow_blank=True)

    class Meta:
        model = RelatedParty
        fields = ["name", "relationship", "balance", "type", "id"]


class BalanceSheetSerializer(serializers.ModelSerializer):
    assets = BalanceAssetSerializer(many=True)
    liabilities = BalanceLiabilitySerializer(many=True)
    debtors = DebtorSerializer(many=True)
    creditors = CreditorSerializer(many=True)
    relatedParties = RelatedPartySerializer(many=True, source="related_parties")

    periodEnd = serializers.DateField(source="period_end")
    shareholdersFunds = serializers.DecimalField(source="shareholders_funds", max_digits=18, decimal_places=2)
    totalAssets = serializers.DecimalField(source="total_assets", max_digits=18, decimal_places=2)
    totalLiabilities = serializers.DecimalField(source="total_liabilities", max_digits=18, decimal_places=2)
    currentAssets = serializers.DecimalField(source="current_assets", max_digits=18, decimal_places=2)
    currentLiabilities = serializers.DecimalField(source="current_liabilities", max_digits=18, decimal_places=2)
    workingCapital = serializers.DecimalField(source="working_capital", max_digits=18, decimal_places=2)
    cashCover = serializers.DecimalField(source="cash_cover", max_digits=18, decimal_places=2)

    class Meta:
        model = BalanceSheet
        fields = [
            "periodEnd",
            "shareholdersFunds",
            "totalAssets",
            "totalLiabilities",
            "currentAssets",
            "currentLiabilities",
            "workingCapital",
            "cashCover",
            "assets",
            "liabilities",
            "debtors",
            "creditors",
            "relatedParties",
        ]

    def create(self, validated_data):
        assets = validated_data.pop("assets", [])
        liabilities = validated_data.pop("liabilities", [])
        debtors = validated_data.pop("debtors", [])
        creditors = validated_data.pop("creditors", [])
        related = validated_data.pop("related_parties", [])
        bs = BalanceSheet.objects.create(**validated_data)
        for a in assets:
            BalanceAsset.objects.create(balance_sheet=bs, **a)
        for l in liabilities:
            BalanceLiability.objects.create(balance_sheet=bs, **l)
        for d in debtors:
            Debtor.objects.create(balance_sheet=bs, **d)
        for c in creditors:
            Creditor.objects.create(balance_sheet=bs, **c)
        for r in related:
            RelatedParty.objects.create(balance_sheet=bs, **r)
        return bs

    def update(self, instance, validated_data):
        assets = validated_data.pop("assets", None)
        liabilities = validated_data.pop("liabilities", None)
        debtors = validated_data.pop("debtors", None)
        creditors = validated_data.pop("creditors", None)
        related = validated_data.pop("related_parties", None)
        for attr, val in validated_data.items():
            setattr(instance, attr, val)
        instance.save()
        if assets is not None:
            instance.assets.all().delete()
            for a in assets:
                BalanceAsset.objects.create(balance_sheet=instance, **a)
        if liabilities is not None:
            instance.liabilities.all().delete()
            for l in liabilities:
                BalanceLiability.objects.create(balance_sheet=instance, **l)
        if debtors is not None:
            instance.debtors.all().delete()
            for d in debtors:
                Debtor.objects.create(balance_sheet=instance, **d)
        if creditors is not None:
            instance.creditors.all().delete()
            for c in creditors:
                Creditor.objects.create(balance_sheet=instance, **c)
        if related is not None:
            instance.related_parties.all().delete()
            for r in related:
                RelatedParty.objects.create(balance_sheet=instance, **r)
        return instance


class ClientAssetSerializer(serializers.ModelSerializer):
    assetType = serializers.CharField(source="asset_type")
    isCurrent = serializers.BooleanField(source="is_current")
    acquisitionDate = serializers.DateField(source="acquisition_date", allow_null=True, required=False)
    concentrationPercentage = serializers.DecimalField(source="concentration_percentage", max_digits=5, decimal_places=2, required=False, allow_null=True)
    id = serializers.CharField(source="frontend_id", required=False, allow_blank=True)

    class Meta:
        model = ClientAsset
        fields = [
            "assetType",
            "category",
            "value",
            "isCurrent",
            "acquisitionDate",
            "id",
            "concentrationPercentage",
        ]


class CapitalPositionSerializer(serializers.ModelSerializer):
    calculationDate = serializers.DateField(source="calculation_date")
    netCapital = serializers.DecimalField(source="net_capital", max_digits=18, decimal_places=2)
    requiredCapital = serializers.DecimalField(source="required_capital", max_digits=18, decimal_places=2)
    adjustedLiquidCapital = serializers.DecimalField(source="adjusted_liquid_capital", max_digits=18, decimal_places=2)
    isCompliant = serializers.BooleanField(source="is_compliant")
    capitalAdequacyRatio = serializers.DecimalField(source="capital_adequacy_ratio", max_digits=7, decimal_places=2, required=False, allow_null=True)

    class Meta:
        model = CapitalPosition
        fields = [
            "calculationDate",
            "netCapital",
            "requiredCapital",
            "adjustedLiquidCapital",
            "isCompliant",
            "capitalAdequacyRatio",
        ]


class SubmissionMetadataSerializer(serializers.ModelSerializer):
    submittedAt = serializers.DateTimeField(source="submitted_at")
    totalBoardMembers = serializers.IntegerField(source="total_board_members")
    totalCommittees = serializers.IntegerField(source="total_committees")
    totalProducts = serializers.IntegerField(source="total_products")
    totalClients = serializers.IntegerField(source="total_clients")
    totalIncomeItems = serializers.IntegerField(source="total_income_items")
    totalAssets = serializers.IntegerField(source="total_assets")
    totalLiabilities = serializers.IntegerField(source="total_liabilities")
    totalClientAssetTypes = serializers.IntegerField(source="total_client_asset_types")
    totalDocuments = serializers.IntegerField(source="total_documents")

    class Meta:
        model = SubmissionMetadata
        fields = [
            "submittedAt",
            "totalBoardMembers",
            "totalCommittees",
            "totalProducts",
            "totalClients",
            "totalIncomeItems",
            "totalAssets",
            "totalLiabilities",
            "totalClientAssetTypes",
            "totalDocuments",
        ]


class SMISubmissionSerializer(serializers.ModelSerializer):
    companyId = serializers.CharField(write_only=True)
    id = serializers.IntegerField(read_only=True)
    reportingPeriod = ReportingPeriodSerializer(source="reporting_period")
    boardMembers = BoardMemberSerializer(many=True, source="board_members")
    committees = CommitteeSerializer(many=True)
    products = ProductSerializer(many=True)
    clients = ClientSerializer(many=True)
    financialStatement = FinancialStatementSerializer()
    balanceSheet = BalanceSheetSerializer()
    clientAssets = ClientAssetSerializer(many=True, source="client_assets")
    capitalPosition = CapitalPositionSerializer()
    metadata = SubmissionMetadataSerializer()
    risk_assessment = RiskAssessmentSerializer(read_only=True)

    class Meta:
        model = SMISubmission
        fields = [
            "id",
            "companyId",
            "reportingPeriod",
            "boardMembers",
            "committees",
            "products",
            "clients",
            "financialStatement",
            "balanceSheet",
            "clientAssets",
            "capitalPosition",
            "metadata",
            "risk_assessment",
        ]

    def create(self, validated_data):
        company_id = validated_data.pop("companyId")
        smi = SMI.objects.filter(license_number=company_id).first() or SMI.objects.filter(id=company_id).first()
        if not smi:
            raise serializers.ValidationError({"companyId": "Company not found"})

        rp_data = validated_data.pop("reporting_period")
        board_members_data = validated_data.pop("board_members", [])
        committees_data = validated_data.pop("committees", [])
        products_data = validated_data.pop("products", [])
        clients_data = validated_data.pop("clients", [])
        financial_stmt_data = validated_data.pop("financial_statement")
        balance_sheet_data = validated_data.pop("balance_sheet")
        client_assets_data = validated_data.pop("client_assets", [])
        capital_position_data = validated_data.pop("capital_position")
        metadata_data = validated_data.pop("metadata")

        reporting_period = ReportingPeriod.objects.create(**rp_data)
        submission = SMISubmission.objects.create(
            smi=smi,
            reporting_period=reporting_period,
            submitted_at=metadata_data.get("submitted_at"),
        )

        # Collections
        for bm in board_members_data:
            BoardMember.objects.create(submission=submission, **bm)
        for c in committees_data:
            Committee.objects.create(submission=submission, **c)
        for p in products_data:
            Product.objects.create(submission=submission, **p)
        for cl in clients_data:
            Client.objects.create(submission=submission, **cl)
        for ca in client_assets_data:
            ClientAsset.objects.create(submission=submission, **ca)

        # One-to-ones
        fs_serializer = FinancialStatementSerializer(data=financial_stmt_data)
        fs_serializer.is_valid(raise_exception=True)
        fs = fs_serializer.save(submission=submission)

        bs_serializer = BalanceSheetSerializer(data=balance_sheet_data)
        bs_serializer.is_valid(raise_exception=True)
        bs_serializer.save(submission=submission)

        CapitalPosition.objects.create(submission=submission, **capital_position_data)

        SubmissionMetadata.objects.create(submission=submission, **metadata_data)

        return submission

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        # Output companyId using license_number when available
        rep["companyId"] = instance.smi.license_number or str(instance.smi.id)
        return rep


