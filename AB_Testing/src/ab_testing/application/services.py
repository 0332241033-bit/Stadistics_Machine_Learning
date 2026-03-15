from __future__ import annotations

from datetime import datetime, timezone

import pandas as pd

from ab_testing.data.data_factory import ExperimentDataFactory
from ab_testing.domain.entities import ExperimentConfig, ExperimentOutcome
from ab_testing.domain.protocols import ExperimentRepository
from ab_testing.infrastructure.estimator_factory import EstimatorFactory
from ab_testing.ml.uplift_model import TLearnerUpliftModel
from ab_testing.stats.validation import ExperimentValidator


class DecisionEngine:
    """Encapsulate release policy and production guardrails."""

    def decide(
        self,
        config: ExperimentConfig,
        conversion_uplift: float,
        conversion_is_significant: bool,
        has_srm_issue: bool,
        has_covariate_imbalance: bool,
    ) -> str:
        if has_srm_issue:
            return "HOLD: Sample Ratio Mismatch detected. Validate traffic split before rollout."

        if has_covariate_imbalance:
            return "HOLD: Covariate imbalance detected. Recheck randomization pipeline."

        if not conversion_is_significant:
            return "CONTINUE TEST: Conversion uplift is not statistically significant yet."

        if conversion_uplift < config.min_detectable_effect:
            return "NO SHIP: Significant uplift is below business MDE threshold."

        return "SHIP TREATMENT: Significant and meaningful conversion uplift detected."


class ExperimentAnalysisService:
    """Service layer orchestrating generation, validation, estimation, and recommendations."""

    def __init__(
        self,
        repository: ExperimentRepository,
        validator: ExperimentValidator,
        uplift_model: TLearnerUpliftModel,
        decision_engine: DecisionEngine | None = None,
        data_factory: ExperimentDataFactory | None = None,
    ) -> None:
        self._repository = repository
        self._validator = validator
        self._uplift_model = uplift_model
        self._decision_engine = decision_engine or DecisionEngine()
        self._data_factory = data_factory or ExperimentDataFactory()

    def run(self, config: ExperimentConfig, regenerate_data: bool = True) -> tuple[ExperimentOutcome, pd.DataFrame]:
        if regenerate_data:
            dataset = self._data_factory.build_dataset(
                sample_size=config.sample_size,
                treatment_share=config.treatment_share,
            )
            self._repository.save(dataset)
        else:
            dataset = self._repository.load()

        validation_result = self._validator.validate(
            dataset,
            expected_treatment_share=config.treatment_share,
        )

        conversion_estimator = EstimatorFactory.create(metric="conversion", alpha=config.alpha)
        revenue_estimator = EstimatorFactory.create(metric="revenue", alpha=config.alpha)

        conversion_result = conversion_estimator.estimate(dataset)
        revenue_result = revenue_estimator.estimate(dataset)

        self._uplift_model.fit(dataset)
        segment_recommendation = self._uplift_model.recommend_top_segment(dataset, top_percent=0.10)

        decision = self._decision_engine.decide(
            config=config,
            conversion_uplift=conversion_result.uplift,
            conversion_is_significant=conversion_result.is_significant,
            has_srm_issue=validation_result.has_srm_issue,
            has_covariate_imbalance=validation_result.has_covariate_imbalance,
        )

        outcome = ExperimentOutcome(
            config=config,
            validation=validation_result,
            conversion_result=conversion_result,
            revenue_result=revenue_result,
            segment_recommendation=segment_recommendation,
            decision=decision,
            generated_at=datetime.now(timezone.utc),
            dataset_size=int(len(dataset)),
        )

        return outcome, dataset
