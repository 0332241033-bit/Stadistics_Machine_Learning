from __future__ import annotations

from dataclasses import asdict
from typing import Any

from ab_testing.domain.entities import ExperimentOutcome


class ExperimentReportBuilder:
    """Build machine-readable and human-readable reports from experiment outcomes."""

    @staticmethod
    def to_dict(outcome: ExperimentOutcome) -> dict[str, Any]:
        payload = asdict(outcome)
        payload["generated_at"] = outcome.generated_at.isoformat()
        payload["config"]["data_path"] = str(outcome.config.data_path)
        payload["config"]["output_dir"] = str(outcome.config.output_dir)
        return payload

    @staticmethod
    def to_markdown(outcome: ExperimentOutcome) -> str:
        conversion = outcome.conversion_result
        revenue = outcome.revenue_result
        validation = outcome.validation
        segment = outcome.segment_recommendation

        return f"""# A/B Experiment Report

## Executive Decision

{outcome.decision}

## Experiment Metadata

- Experiment: {outcome.config.experiment_name}
- Generated at (UTC): {outcome.generated_at.isoformat()}
- Sample size: {outcome.dataset_size}
- Alpha: {outcome.config.alpha:.3f}
- MDE: {outcome.config.min_detectable_effect:.2%}

## Experiment Quality Checks

- SRM p-value: {validation.srm_p_value:.6f}
- SRM issue detected: {validation.has_srm_issue}
- Max absolute SMD: {validation.max_abs_smd:.4f}
- Covariate imbalance detected: {validation.has_covariate_imbalance}

## Conversion Effect (Primary Metric)

- Control conversion: {conversion.control_mean:.4%}
- Treatment conversion: {conversion.treatment_mean:.4%}
- Absolute uplift: {conversion.uplift:.4%}
- 95% CI: [{conversion.ci_low:.4%}, {conversion.ci_high:.4%}]
- p-value: {conversion.p_value:.6f}
- Statistically significant: {conversion.is_significant}

## Revenue Effect (Secondary Metric, CUPED)

- Control revenue/user: {revenue.control_mean:.4f}
- Treatment revenue/user: {revenue.treatment_mean:.4f}
- Revenue uplift: {revenue.uplift:.4f}
- 95% CI: [{revenue.ci_low:.4f}, {revenue.ci_high:.4f}]
- p-value: {revenue.p_value:.6f}
- Statistically significant: {revenue.is_significant}
- CUPED theta: {revenue.extra.get('theta', 0.0):.6f}
- Variance reduction: {revenue.extra.get('variance_reduction', 0.0):.2%}

## Uplift Targeting Recommendation

- Segment: {segment.segment_name}
- Segment users: {segment.size}
- Avg predicted uplift: {segment.avg_uplift:.4%}
- Expected incremental conversions: {segment.expected_incremental_conversions:.2f}
"""
