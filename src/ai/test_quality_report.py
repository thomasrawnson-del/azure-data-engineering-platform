import pandas as pd

from src.ai.quality_report import build_quality_report


def test_build_quality_report():
    orders = pd.DataFrame(
        {
            "order_id": [10006, 10007],
            "validation_error": [
                "Quantity must be greater than zero; ",
                "Missing customer ID; ",
            ],
        }
    )

    report = build_quality_report(orders)

    assert len(report) == 2
    assert "category" in report.columns
    assert "severity" in report.columns
    assert "recommendation" in report.columns