from decimal import Decimal
from django.db import transaction
from apps.smi_module.models import SMISubmission, RiskAssessment


def _calculate_credit_risk(submission: SMISubmission):
    # TODO: [USER MUST PROVIDE FORMULA]
    score = Decimal("0.0")
    rating = "Not Calculated"
    weight = Decimal("0.000")
    return weight, score, rating


def _calculate_market_risk(submission: SMISubmission):
    # TODO: [USER MUST PROVIDE FORMULA]
    score = Decimal("0.0")
    rating = "Not Calculated"
    weight = Decimal("0.000")
    return weight, score, rating


def _calculate_liquidity_risk(submission: SMISubmission):
    # TODO: [USER MUST PROVIDE FORMULA]
    score = Decimal("0.0")
    rating = "Not Calculated"
    weight = Decimal("0.000")
    return weight, score, rating


def _calculate_operational_risk(submission: SMISubmission):
    # TODO: [USER MUST PROVIDE FORMULA]
    score = Decimal("0.0")
    rating = "Not Calculated"
    weight = Decimal("0.000")
    return weight, score, rating


def _calculate_legal_risk(submission: SMISubmission):
    # TODO: [USER MUST PROVIDE FORMULA]
    score = Decimal("0.0")
    rating = "Not Calculated"
    weight = Decimal("0.000")
    return weight, score, rating


def _calculate_compliance_risk(submission: SMISubmission):
    # TODO: [USER MUST PROVIDE FORMULA]
    score = Decimal("0.0")
    rating = "Not Calculated"
    weight = Decimal("0.000")
    return weight, score, rating


def _calculate_strategic_risk(submission: SMISubmission):
    # TODO: [USER MUST PROVIDE FORMULA]
    score = Decimal("0.0")
    rating = "Not Calculated"
    weight = Decimal("0.000")
    return weight, score, rating


def _calculate_reputation_risk(submission: SMISubmission):
    # TODO: [USER MUST PROVIDE FORMULA]
    score = Decimal("0.0")
    rating = "Not Calculated"
    weight = Decimal("0.000")
    return weight, score, rating


def _calculate_fsi_score(scores: list[Decimal]) -> Decimal:
    # TODO: [USER MUST PROVIDE FORMULA]
    return Decimal("0.0")


@transaction.atomic
def calculate_risk_assessment(submission_id: int) -> RiskAssessment:
    submission = SMISubmission.objects.select_related(
        'financial_statement', 'balance_sheet', 'capital_position'
    ).prefetch_related(
        'board_members','committees','products','clients',
        'balance_sheet__assets','balance_sheet__liabilities','balance_sheet__debtors',
        'balance_sheet__creditors','balance_sheet__related_parties','client_assets'
    ).get(id=submission_id)

    credit_w, credit_s, credit_r = _calculate_credit_risk(submission)
    market_w, market_s, market_r = _calculate_market_risk(submission)
    liquidity_w, liquidity_s, liquidity_r = _calculate_liquidity_risk(submission)
    operational_w, operational_s, operational_r = _calculate_operational_risk(submission)
    legal_w, legal_s, legal_r = _calculate_legal_risk(submission)
    compliance_w, compliance_s, compliance_r = _calculate_compliance_risk(submission)
    strategic_w, strategic_s, strategic_r = _calculate_strategic_risk(submission)
    reputation_w, reputation_s, reputation_r = _calculate_reputation_risk(submission)

    fsi = _calculate_fsi_score([
        credit_s, market_s, liquidity_s, operational_s,
        legal_s, compliance_s, strategic_s, reputation_s
    ])

    # Placeholder composite rating logic; to be replaced by user-provided method
    composite = "Not Calculated"

    ra, _created = RiskAssessment.objects.update_or_create(
        submission=submission,
        defaults={
            'credit_risk_weight': credit_w, 'credit_risk_score': credit_s, 'credit_risk_rating': credit_r,
            'market_risk_weight': market_w, 'market_risk_score': market_s, 'market_risk_rating': market_r,
            'liquidity_risk_weight': liquidity_w, 'liquidity_risk_score': liquidity_s, 'liquidity_risk_rating': liquidity_r,
            'operational_risk_weight': operational_w, 'operational_risk_score': operational_s, 'operational_risk_rating': operational_r,
            'legal_risk_weight': legal_w, 'legal_risk_score': legal_s, 'legal_risk_rating': legal_r,
            'compliance_risk_weight': compliance_w, 'compliance_risk_score': compliance_s, 'compliance_risk_rating': compliance_r,
            'strategic_risk_weight': strategic_w, 'strategic_risk_score': strategic_s, 'strategic_risk_rating': strategic_r,
            'reputation_risk_weight': reputation_w, 'reputation_risk_score': reputation_s, 'reputation_risk_rating': reputation_r,
            'composite_risk_rating': composite,
            'fsi_score': fsi,
        }
    )

    return ra


