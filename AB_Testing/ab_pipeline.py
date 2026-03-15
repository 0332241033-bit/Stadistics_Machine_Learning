from __future__ import annotations

import argparse
import json
import logging
import sys
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent
SRC_ROOT = PROJECT_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from ab_testing.application.services import ExperimentAnalysisService
from ab_testing.data.repository import CsvExperimentRepository
from ab_testing.domain.entities import ExperimentConfig
from ab_testing.ml.uplift_model import TLearnerUpliftModel
from ab_testing.reporting.report_builder import ExperimentReportBuilder
from ab_testing.stats.validation import ExperimentValidator


logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Professional ML-powered A/B testing pipeline")
    parser.add_argument("--experiment-name", type=str, default="checkout_redesign_experiment")
    parser.add_argument("--sample-size", type=int, default=12000)
    parser.add_argument("--treatment-share", type=float, default=0.5)
    parser.add_argument("--alpha", type=float, default=0.05)
    parser.add_argument("--mde", type=float, default=0.01, help="Minimum detectable effect (absolute)")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument(
        "--use-existing-data",
        action="store_true",
        help="Load existing CSV data instead of generating a new synthetic sample",
    )
    return parser.parse_args()


def build_config(args: argparse.Namespace) -> ExperimentConfig:
    return ExperimentConfig(
        experiment_name=args.experiment_name,
        seed=args.seed,
        sample_size=args.sample_size,
        treatment_share=args.treatment_share,
        alpha=args.alpha,
        min_detectable_effect=args.mde,
        data_path=PROJECT_ROOT / "data" / "ab_experiment.csv",
        output_dir=PROJECT_ROOT / "outputs",
    )


def main() -> None:
    args = parse_args()
    config = build_config(args)

    repository = CsvExperimentRepository(config.data_path)
    validator = ExperimentValidator(alpha=config.alpha)
    uplift_model = TLearnerUpliftModel(seed=config.seed)

    analysis_service = ExperimentAnalysisService(
        repository=repository,
        validator=validator,
        uplift_model=uplift_model,
    )

    outcome, dataset = analysis_service.run(config=config, regenerate_data=not args.use_existing_data)

    config.output_dir.mkdir(parents=True, exist_ok=True)

    report_builder = ExperimentReportBuilder()
    outcome_payload = report_builder.to_dict(outcome)
    outcome_json_path = config.output_dir / "experiment_outcome.json"
    report_md_path = config.output_dir / "experiment_report.md"

    outcome_json_path.write_text(json.dumps(outcome_payload, indent=2), encoding="utf-8")
    report_md_path.write_text(report_builder.to_markdown(outcome), encoding="utf-8")

    variant_summary = (
        dataset.groupby("variant", as_index=False)
        .agg(
            users=("user_id", "count"),
            conversion_rate=("converted", "mean"),
            avg_revenue=("revenue", "mean"),
        )
        .sort_values("variant")
    )

    summary_path = config.output_dir / "variant_summary.csv"
    variant_summary.to_csv(summary_path, index=False)

    logging.info("A/B testing run finished")
    logging.info("Dataset path: %s", config.data_path)
    logging.info("Outcome JSON: %s", outcome_json_path)
    logging.info("Markdown report: %s", report_md_path)
    logging.info("Variant summary CSV: %s", summary_path)

    print("\n=== Experiment Decision ===")
    print(outcome.decision)

    print("\n=== Conversion Lift ===")
    print(f"Control:   {outcome.conversion_result.control_mean:.4%}")
    print(f"Treatment: {outcome.conversion_result.treatment_mean:.4%}")
    print(f"Uplift:    {outcome.conversion_result.uplift:.4%}")
    print(f"p-value:   {outcome.conversion_result.p_value:.6f}")

    print("\n=== Revenue Lift (CUPED) ===")
    print(f"Control:   {outcome.revenue_result.control_mean:.4f}")
    print(f"Treatment: {outcome.revenue_result.treatment_mean:.4f}")
    print(f"Uplift:    {outcome.revenue_result.uplift:.4f}")
    print(f"p-value:   {outcome.revenue_result.p_value:.6f}")

    print("\n=== Uplift Segment Recommendation ===")
    print(f"Segment: {outcome.segment_recommendation.segment_name}")
    print(f"Users:   {outcome.segment_recommendation.size}")
    print(f"Avg uplift: {outcome.segment_recommendation.avg_uplift:.4%}")


if __name__ == "__main__":
    main()
