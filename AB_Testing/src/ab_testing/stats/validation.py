from __future__ import annotations

import math

import pandas as pd

from ab_testing.domain.entities import ValidationResult


class ExperimentValidator:
    """Validate randomization quality and covariate balance."""

    DEFAULT_BALANCE_FEATURES = [
        "days_since_signup",
        "prior_orders_30d",
        "prior_sessions_7d",
        "prior_avg_basket",
        "pre_period_revenue",
    ]

    def __init__(self, alpha: float = 0.05) -> None:
        self.alpha = alpha

    @staticmethod
    def _chi_square_p_value_df1(chi_square_stat: float) -> float:
        # For df=1, survival function can be computed exactly using erfc.
        return math.erfc(math.sqrt(max(chi_square_stat, 0.0) / 2.0))

    @staticmethod
    def _standardized_mean_difference(control: pd.Series, treatment: pd.Series) -> float:
        control_var = float(control.var(ddof=1))
        treatment_var = float(treatment.var(ddof=1))
        pooled_std = math.sqrt(max((control_var + treatment_var) / 2.0, 0.0))
        if pooled_std == 0.0:
            return 0.0
        return float((treatment.mean() - control.mean()) / pooled_std)

    def validate(self, df: pd.DataFrame, expected_treatment_share: float) -> ValidationResult:
        if not 0 < expected_treatment_share < 1:
            raise ValueError("expected_treatment_share must be between 0 and 1")

        total = len(df)
        observed_treatment = int(df["is_treatment"].sum())
        observed_control = int(total - observed_treatment)

        expected_treatment = total * expected_treatment_share
        expected_control = total * (1.0 - expected_treatment_share)

        if expected_treatment == 0 or expected_control == 0:
            raise ValueError("Expected counts cannot be zero")

        chi_square = (
            ((observed_treatment - expected_treatment) ** 2) / expected_treatment
            + ((observed_control - expected_control) ** 2) / expected_control
        )
        srm_p_value = self._chi_square_p_value_df1(float(chi_square))

        covariate_smd: dict[str, float] = {}
        for feature in self.DEFAULT_BALANCE_FEATURES:
            if feature not in df.columns:
                continue
            control_group = df.loc[df["is_treatment"] == 0, feature].astype(float)
            treatment_group = df.loc[df["is_treatment"] == 1, feature].astype(float)
            covariate_smd[feature] = self._standardized_mean_difference(control_group, treatment_group)

        max_abs_smd = max((abs(value) for value in covariate_smd.values()), default=0.0)

        return ValidationResult(
            srm_p_value=float(srm_p_value),
            has_srm_issue=bool(srm_p_value < self.alpha),
            max_abs_smd=float(max_abs_smd),
            has_covariate_imbalance=bool(max_abs_smd > 0.10),
            covariate_smd=covariate_smd,
        )
