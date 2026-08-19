from dataclasses import dataclass

import pandas as pd

from src.ai.bedrock_client import invoke_bedrock


@dataclass
class QualityInsight:
    category: str
    severity: str
    affected_records: int
    recommendation: str


def _build_rule_based_insights(
    invalid_orders: pd.DataFrame,
) -> list[QualityInsight]:
    """Identify data quality issues using deterministic rules."""

    insights: list[QualityInsight] = []

    if invalid_orders.empty:
        return insights

    errors = invalid_orders["validation_error"].fillna("")

    duplicate_count = int(
        errors.str.contains(
            "Duplicate order ID",
            regex=False,
        ).sum()
    )

    if duplicate_count:
        insights.append(
            QualityInsight(
                category="Duplicate Records",
                severity="High",
                affected_records=duplicate_count,
                recommendation=(
                    "Investigate the source system for duplicate "
                    "order submissions before reprocessing."
                ),
            )
        )

    missing_customer_count = int(
        errors.str.contains(
            "Missing customer ID",
            regex=False,
        ).sum()
    )

    if missing_customer_count:
        insights.append(
            QualityInsight(
                category="Missing Required Field",
                severity="High",
                affected_records=missing_customer_count,
                recommendation=(
                    "Populate customer_id from the source system "
                    "before the record is reprocessed."
                ),
            )
        )

    invalid_quantity_count = int(
        errors.str.contains(
            "Quantity must be greater than zero",
            regex=False,
        ).sum()
    )

    if invalid_quantity_count:
        insights.append(
            QualityInsight(
                category="Invalid Quantity",
                severity="Medium",
                affected_records=invalid_quantity_count,
                recommendation=(
                    "Check the source order quantity and ensure "
                    "it is greater than zero before reprocessing."
                ),
            )
        )

    invalid_date_count = int(
        errors.str.contains(
            "Invalid order date",
            regex=False,
        ).sum()
    )

    if invalid_date_count:
        insights.append(
            QualityInsight(
                category="Invalid Date",
                severity="Medium",
                affected_records=invalid_date_count,
                recommendation=(
                    "Validate the source date format and convert "
                    "the value to the expected ISO date format."
                ),
            )
        )

    missing_price_count = int(
        errors.str.contains(
            "Missing unit price",
            regex=False,
        ).sum()
    )

    if missing_price_count:
        insights.append(
            QualityInsight(
                category="Missing Required Field",
                severity="High",
                affected_records=missing_price_count,
                recommendation=(
                    "Populate unit_price from the source system "
                    "before the record is reprocessed."
                ),
            )
        )

    return insights


def _build_ai_prompt(
    insights: list[QualityInsight],
) -> str:
    """Build a prompt for Bedrock using the detected quality issues."""

    issue_text = "\n".join(
        (
            f"- Category: {insight.category}\n"
            f"  Severity: {insight.severity}\n"
            f"  Affected records: {insight.affected_records}\n"
            f"  Current recommendation: {insight.recommendation}"
        )
        for insight in insights
    )

    return f"""
You are a senior data engineer reviewing a data quality report.

Review the following detected data quality issues:

{issue_text}

For each issue, provide an improved practical recommendation for
resolving the problem in the source data pipeline.

Keep the recommendations concise and actionable.

Do not invent data or change the category, severity, or number of
affected records.

Return only a numbered list of recommendations.
""".strip()


def _enhance_with_ai(
    insights: list[QualityInsight],
) -> list[QualityInsight]:
    """Use Amazon Bedrock to improve quality recommendations."""

    if not insights:
        return insights

    prompt = _build_ai_prompt(insights)

    try:
        response = invoke_bedrock(prompt)

    except Exception as exc:
        print(
            f"Bedrock analysis unavailable; "
            f"using rule-based recommendations: {exc}"
        )
        return insights

    recommendations = [
        line.strip()
        for line in response.splitlines()
        if line.strip()
    ]

    enhanced_insights: list[QualityInsight] = []

    for index, insight in enumerate(insights):
        recommendation = insight.recommendation

        if index < len(recommendations):
            recommendation = recommendations[index]

        enhanced_insights.append(
            QualityInsight(
                category=insight.category,
                severity=insight.severity,
                affected_records=insight.affected_records,
                recommendation=recommendation,
            )
        )

    return enhanced_insights


def analyze_quality_issues(
    invalid_orders: pd.DataFrame,
    use_ai: bool = True,
) -> list[QualityInsight]:
    """
    Analyse validation errors and produce data quality insights.

    Deterministic rules identify the issues. Amazon Bedrock can then
    improve the recommendations. If Bedrock is unavailable, the
    deterministic recommendations are returned instead.
    """

    insights = _build_rule_based_insights(invalid_orders)

    if not use_ai:
        return insights

    return _enhance_with_ai(insights)