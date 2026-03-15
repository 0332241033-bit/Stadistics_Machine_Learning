from __future__ import annotations

import math
from statistics import NormalDist

import numpy as np
import pandas as pd

from ab_testing.domain.entities import EstimationResult


def _confidence_interval_bounds(uplift: float, standard_error: float, alpha: float) -> tuple[float, float]:
    if standard_error <= 0:
        return uplift, uplift
    z_critical = NormalDist().inv_cdf(1.0 - (alpha / 2.0))
    margin = z_critical * standard_error
    return uplift - margin, uplift + margin


def _two_sided_p_value(z_score: float) -> float:
    return 2.0 * (1.0 - NormalDist().cdf(abs(z_score)))


class DifferenceInMeansEstimator:
    """Frequentist estimator for average treatment effect using mean differences."""

    def __init__(
        self,
        metric_column: str,
        alpha: float = 0.05,
        binary_metric: bool = False,
        metric_name: str | None = None,
    ) -> None:
        self.metric_column = metric_column
        self.alpha = alpha
        self.binary_metric = binary_metric
        self.metric_name = metric_name or metric_column

    def estimate(self, df: pd.DataFrame) -> EstimationResult:
        treatment = df.loc[df["is_treatment"] == 1, self.metric_column].astype(float)
        control = df.loc[df["is_treatment"] == 0, self.metric_column].astype(float)

        if treatment.empty or control.empty:
            raise ValueError("Both treatment and control groups must contain observations")

        treatment_mean = float(treatment.mean())
        control_mean = float(control.mean())
        uplift = treatment_mean - control_mean

        if self.binary_metric:
            treatment_var = treatment_mean * (1.0 - treatment_mean) / len(treatment)
            control_var = control_mean * (1.0 - control_mean) / len(control)
        else:
            treatment_var = float(treatment.var(ddof=1) / len(treatment))
            control_var = float(control.var(ddof=1) / len(control))

        standard_error = math.sqrt(max(treatment_var + control_var, 0.0))

        if standard_error <= 1e-12:
            z_score = 0.0
            p_value = 1.0 if math.isclose(uplift, 0.0, abs_tol=1e-12) else 0.0
        else:
            z_score = uplift / standard_error
            p_value = _two_sided_p_value(z_score)

        ci_low, ci_high = _confidence_interval_bounds(uplift, standard_error, self.alpha)

        return EstimationResult(
            metric=self.metric_name,
            control_mean=control_mean,
            treatment_mean=treatment_mean,
            uplift=uplift,
            ci_low=ci_low,
            ci_high=ci_high,
            p_value=float(p_value),
            is_significant=bool(p_value < self.alpha),
            extra={
                "standard_error": float(standard_error),
                "z_score": float(z_score),
                "n_treatment": int(len(treatment)),
                "n_control": int(len(control)),
            },
        )


class CupedDifferenceInMeansEstimator:
    """CUPED-adjusted mean difference estimator for variance reduction."""

    def __init__(
        self,
        metric_column: str,
        covariate_column: str,
        alpha: float = 0.05,
        metric_name: str | None = None,
    ) -> None:
        self.metric_column = metric_column
        self.covariate_column = covariate_column
        self.alpha = alpha
        self.metric_name = metric_name or f"{metric_column}_cuped"

    def estimate(self, df: pd.DataFrame) -> EstimationResult:
        y = df[self.metric_column].astype(float)
        x = df[self.covariate_column].astype(float)

        var_x = float(np.var(x, ddof=1))
        if abs(var_x) <= 1e-12:
            theta = 0.0
        else:
            theta = float(np.cov(y, x, ddof=1)[0, 1] / var_x)

        adjusted_metric = y - theta * (x - float(x.mean()))
        adjusted_df = df.copy()
        adjusted_df[self.metric_column] = adjusted_metric

        base_estimator = DifferenceInMeansEstimator(
            metric_column=self.metric_column,
            alpha=self.alpha,
            binary_metric=False,
            metric_name=self.metric_name,
        )
        result = base_estimator.estimate(adjusted_df)

        raw_variance = float(np.var(y, ddof=1))
        adjusted_variance = float(np.var(adjusted_metric, ddof=1))
        variance_reduction = 0.0
        if raw_variance > 0:
            variance_reduction = max(0.0, 1.0 - (adjusted_variance / raw_variance))

        result.extra["theta"] = theta
        result.extra["raw_variance"] = raw_variance
        result.extra["adjusted_variance"] = adjusted_variance
        result.extra["variance_reduction"] = variance_reduction

        return result
