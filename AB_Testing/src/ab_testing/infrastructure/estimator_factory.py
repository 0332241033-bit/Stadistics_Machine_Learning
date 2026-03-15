from __future__ import annotations

from ab_testing.domain.protocols import TreatmentEffectEstimator
from ab_testing.stats.estimators import CupedDifferenceInMeansEstimator, DifferenceInMeansEstimator


class EstimatorFactory:
    """Factory that returns the estimator strategy based on metric name."""

    @staticmethod
    def create(metric: str, alpha: float) -> TreatmentEffectEstimator:
        metric_key = metric.lower().strip()

        if metric_key == "conversion":
            return DifferenceInMeansEstimator(
                metric_column="converted",
                alpha=alpha,
                binary_metric=True,
                metric_name="conversion_rate",
            )

        if metric_key == "revenue":
            return CupedDifferenceInMeansEstimator(
                metric_column="revenue",
                covariate_column="pre_period_revenue",
                alpha=alpha,
                metric_name="revenue_per_user_cuped",
            )

        raise ValueError(f"Unsupported metric for estimator factory: {metric}")
