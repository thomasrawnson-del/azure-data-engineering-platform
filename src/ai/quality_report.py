import pandas as pd

from src.ai.quality_analyzer import analyze_quality_issues


def build_quality_report(
    invalid_orders: pd.DataFrame,
) -> pd.DataFrame:
    """Build a tabular data-quality report from invalid orders."""

    insights = analyze_quality_issues(invalid_orders)

    if not insights:
        return pd.DataFrame(
            columns=[
                "category",
                "severity",
                "affected_records",
                "recommendation",
            ]
        )

    return pd.DataFrame(
        [
            {
                "category": insight.category,
                "severity": insight.severity,
                "affected_records": insight.affected_records,
                "recommendation": insight.recommendation,
            }
            for insight in insights
        ]
    )