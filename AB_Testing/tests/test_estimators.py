from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

SRC_ROOT = Path(__file__).resolve().parents[1] / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from ab_testing.stats.estimators import CupedDifferenceInMeansEstimator, DifferenceInMeansEstimator


def test_difference_in_means_binary_returns_positive_uplift() -> None:
    df = pd.DataFrame(
        {
            "is_treatment": [0, 0, 0, 0, 1, 1, 1, 1],
            "converted": [0, 0, 1, 0, 1, 1, 1, 0],
        }
    )

    estimator = DifferenceInMeansEstimator(
        metric_column="converted",
        alpha=0.05,
        binary_metric=True,
        metric_name="conversion_rate",
    )
    result = estimator.estimate(df)

    assert result.metric == "conversion_rate"
    assert result.uplift > 0
    assert result.treatment_mean > result.control_mean
    assert 0 <= result.p_value <= 1


def test_cuped_estimator_adds_variance_reduction_metadata() -> None:
    df = pd.DataFrame(
        {
            "is_treatment": [0, 0, 0, 0, 1, 1, 1, 1],
            "pre_period_revenue": [85, 90, 70, 100, 88, 96, 93, 105],
            "revenue": [21, 23, 18, 25, 25, 28, 27, 31],
        }
    )

    estimator = CupedDifferenceInMeansEstimator(
        metric_column="revenue",
        covariate_column="pre_period_revenue",
        alpha=0.05,
        metric_name="revenue_per_user_cuped",
    )
    result = estimator.estimate(df)

    assert result.metric == "revenue_per_user_cuped"
    assert "theta" in result.extra
    assert "variance_reduction" in result.extra
    assert result.extra["variance_reduction"] >= 0
