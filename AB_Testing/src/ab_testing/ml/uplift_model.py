from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier

from ab_testing.domain.entities import UpliftSegmentResult


class TLearnerUpliftModel:
    """Two-model uplift estimator (T-Learner) for heterogeneous treatment effects."""

    FEATURE_COLUMNS = [
        "device",
        "country_tier",
        "days_since_signup",
        "prior_orders_30d",
        "prior_sessions_7d",
        "prior_avg_basket",
        "pre_period_revenue",
    ]
    CATEGORICAL_COLUMNS = ["device", "country_tier"]

    def __init__(self, seed: int = 42) -> None:
        self._seed = seed
        self._treatment_model = GradientBoostingClassifier(
            random_state=seed,
            learning_rate=0.05,
            n_estimators=150,
            max_depth=3,
        )
        self._control_model = GradientBoostingClassifier(
            random_state=seed + 1,
            learning_rate=0.05,
            n_estimators=150,
            max_depth=3,
        )
        self._feature_columns: list[str] | None = None

    def _prepare_features(self, df: pd.DataFrame, fit: bool = False) -> pd.DataFrame:
        missing_columns = [column for column in self.FEATURE_COLUMNS if column not in df.columns]
        if missing_columns:
            raise ValueError(f"Missing required feature columns: {missing_columns}")

        raw_features = df[self.FEATURE_COLUMNS].copy()
        encoded = pd.get_dummies(raw_features, columns=self.CATEGORICAL_COLUMNS, drop_first=True)

        if fit or self._feature_columns is None:
            self._feature_columns = encoded.columns.tolist()
            return encoded

        return encoded.reindex(columns=self._feature_columns, fill_value=0.0)

    def fit(self, df: pd.DataFrame) -> None:
        if "converted" not in df.columns or "is_treatment" not in df.columns:
            raise ValueError("Input dataframe must contain converted and is_treatment columns")

        x = self._prepare_features(df, fit=True)
        y = df["converted"].astype(int)

        treatment_mask = df["is_treatment"] == 1
        control_mask = df["is_treatment"] == 0

        if treatment_mask.sum() < 50 or control_mask.sum() < 50:
            raise ValueError("Both groups require at least 50 observations for uplift modeling")

        self._treatment_model.fit(x.loc[treatment_mask], y.loc[treatment_mask])
        self._control_model.fit(x.loc[control_mask], y.loc[control_mask])

    def predict_uplift(self, df: pd.DataFrame) -> pd.Series:
        x = self._prepare_features(df, fit=False)
        treatment_prob = self._treatment_model.predict_proba(x)[:, 1]
        control_prob = self._control_model.predict_proba(x)[:, 1]
        uplift = treatment_prob - control_prob
        return pd.Series(uplift, index=df.index, name="uplift_score")

    def recommend_top_segment(self, df: pd.DataFrame, top_percent: float = 0.10) -> UpliftSegmentResult:
        if not 0 < top_percent < 1:
            raise ValueError("top_percent must be between 0 and 1")

        uplift_scores = self.predict_uplift(df)
        threshold = float(np.quantile(uplift_scores, 1.0 - top_percent))
        segment_mask = uplift_scores >= threshold

        segment_size = int(segment_mask.sum())
        avg_uplift = float(uplift_scores.loc[segment_mask].mean()) if segment_size > 0 else 0.0
        expected_incremental_conversions = float(avg_uplift * segment_size)

        return UpliftSegmentResult(
            segment_name=f"Top {int(top_percent * 100)}% users by predicted uplift",
            size=segment_size,
            avg_uplift=avg_uplift,
            expected_incremental_conversions=expected_incremental_conversions,
        )
