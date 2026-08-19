from dataclasses import dataclass

import pandas as pd


@dataclass
class QualityInsight:
    category: str
    severity: str
    affected_records: int
    recommendation: str


def analyze_quality_issues(
    invalid_orders: pd.DataFrame,
) -> list[QualityInsight]:
    """
    Analyse validation errors and produce data quality insights.

    This is the initial implementation of the AI analysis interface.
    The underlying analysis is rule-based so that the pipeline remains
    deterministic and does not require an external LLM service.
    """

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