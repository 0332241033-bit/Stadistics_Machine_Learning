from __future__ import annotations

import numpy as np
import pandas as pd

from ab_testing.domain.entities import Variant


class ExperimentDataFactory:
    """Generate realistic synthetic data for checkout experiments."""

    def __init__(self, seed: int = 42) -> None:
        self._rng = np.random.default_rng(seed)

    def build_dataset(self, sample_size: int, treatment_share: float = 0.5) -> pd.DataFrame:
        if sample_size <= 0:
            raise ValueError("sample_size must be greater than zero")
        if not 0 < treatment_share < 1:
            raise ValueError("treatment_share must be between 0 and 1")

        rng = self._rng

        user_id = np.arange(1, sample_size + 1)
        device = rng.choice(["mobile", "desktop", "tablet"], size=sample_size, p=[0.62, 0.30, 0.08])
        country_tier = rng.choice(["tier1", "tier2", "tier3"], size=sample_size, p=[0.50, 0.35, 0.15])

        days_since_signup = rng.integers(1, 720, size=sample_size)
        prior_orders_30d = rng.poisson(2.3, size=sample_size)
        prior_sessions_7d = rng.poisson(8.0, size=sample_size) + 1
        prior_avg_basket = np.clip(rng.normal(68.0, 18.0, size=sample_size), 5.0, None)

        pre_period_revenue = np.clip(
            prior_orders_30d * prior_avg_basket * rng.normal(1.0, 0.22, size=sample_size),
            0.0,
            None,
        )

        is_treatment = rng.binomial(1, treatment_share, size=sample_size)
        variant = np.where(is_treatment == 1, Variant.TREATMENT.value, Variant.CONTROL.value)

        baseline_logit = (
            -2.2
            + 0.12 * np.log1p(prior_orders_30d)
            + 0.08 * np.log1p(prior_sessions_7d)
            + 0.18 * (country_tier == "tier1")
            + 0.07 * (device == "desktop")
            + 0.0015 * days_since_signup
            + 0.005 * np.clip(prior_avg_basket / 10.0, 0, 20)
        )

        baseline_prob = 1.0 / (1.0 + np.exp(-baseline_logit))

        treatment_effect = (
            0.010
            + 0.020 * (device == "mobile")
            + 0.012 * (country_tier == "tier2")
            - 0.008 * (prior_orders_30d >= 6)
        )

        conversion_prob = np.clip(baseline_prob + is_treatment * treatment_effect, 0.001, 0.99)
        converted = rng.binomial(1, conversion_prob, size=sample_size)

        order_noise = np.clip(rng.lognormal(mean=3.35, sigma=0.38, size=sample_size), 3.0, None)
        base_order_value = np.clip(prior_avg_basket * rng.normal(1.0, 0.18, size=sample_size), 5.0, None)
        revenue = converted * np.clip(base_order_value + 0.10 * order_noise, 0.0, None)

        revenue = revenue * (1.0 + is_treatment * (0.030 + 0.010 * (device == "desktop")))

        session_date = pd.Timestamp("2026-01-01") + pd.to_timedelta(
            rng.integers(0, 60, size=sample_size),
            unit="D",
        )

        data = pd.DataFrame(
            {
                "user_id": user_id,
                "session_date": session_date,
                "variant": variant,
                "is_treatment": is_treatment.astype(int),
                "device": device,
                "country_tier": country_tier,
                "days_since_signup": days_since_signup.astype(int),
                "prior_orders_30d": prior_orders_30d.astype(int),
                "prior_sessions_7d": prior_sessions_7d.astype(int),
                "prior_avg_basket": prior_avg_basket.astype(float),
                "pre_period_revenue": pre_period_revenue.astype(float),
                "converted": converted.astype(int),
                "revenue": revenue.astype(float),
            }
        )

        return data
