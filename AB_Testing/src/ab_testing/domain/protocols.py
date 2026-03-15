from __future__ import annotations

from typing import Protocol

import pandas as pd

from ab_testing.domain.entities import EstimationResult


class ExperimentRepository(Protocol):
    def save(self, df: pd.DataFrame) -> None:
        ...

    def load(self) -> pd.DataFrame:
        ...


class TreatmentEffectEstimator(Protocol):
    metric_name: str

    def estimate(self, df: pd.DataFrame) -> EstimationResult:
        ...
