import pandas as pd

from src.ai.quality_analyzer import analyze_quality_issues


def test_quality_analyzer_detects_invalid_orders():
    orders = pd.DataFrame(
        {
            "order_id": [10006, 10007, 10008],
            "validation_error": [
                "Quantity must be greater than zero; ",
                "Missing customer ID; ",
                "Invalid order date; ",
            ],
        }
    )

    insights = analyze_quality_issues(
        orders,
        use_ai=False,
)   

    assert len(insights) == 3

    categories = {
        insight.category
        for insight in insights
    }

    assert "Invalid Quantity" in categories
    assert "Missing Required Field" in categories
    assert "Invalid Date" in categories