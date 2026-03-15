from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any


class Variant(str, Enum):
    CONTROL = "control"
    TREATMENT = "treatment"


@dataclass(frozen=True)
class ExperimentConfig:
    experiment_name: str = "checkout_redesign_experiment"
    seed: int = 42
    sample_size: int = 12000
    treatment_share: float = 0.5
    alpha: float = 0.05
    min_detectable_effect: float = 0.01
    data_path: Path = Path("AB_Testing/data/ab_experiment.csv")
    output_dir: Path = Path("AB_Testing/outputs")


@dataclass
class EstimationResult:
    metric: str
    control_mean: float
    treatment_mean: float
    uplift: float
    ci_low: float
    ci_high: float
    p_value: float
    is_significant: bool
    extra: dict[str, Any] = field(default_factory=dict)


@dataclass
class ValidationResult:
    srm_p_value: float
    has_srm_issue: bool
    max_abs_smd: float
    has_covariate_imbalance: bool
    covariate_smd: dict[str, float] = field(default_factory=dict)


@dataclass
class UpliftSegmentResult:
    segment_name: str
    size: int
    avg_uplift: float
    expected_incremental_conversions: float


@dataclass
class ExperimentOutcome:
    config: ExperimentConfig
    validation: ValidationResult
    conversion_result: EstimationResult
    revenue_result: EstimationResult
    segment_recommendation: UpliftSegmentResult
    decision: str
    generated_at: datetime
    dataset_size: int
