from __future__ import annotations

import json
import sys
from pathlib import Path

import pandas as pd
import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parent
SRC_ROOT = PROJECT_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from ab_testing.ml.uplift_model import TLearnerUpliftModel


st.set_page_config(page_title="A/B Testing Command Center", layout="wide")


@st.cache_data
def load_outcome_json(outcome_path: str) -> dict | None:
    path = Path(outcome_path)
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


@st.cache_data
def load_dataset(data_path: str) -> pd.DataFrame:
    path = Path(data_path)
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path)


@st.cache_data
def compute_uplift_deciles(df: pd.DataFrame, seed: int) -> pd.DataFrame:
    model = TLearnerUpliftModel(seed=seed)
    model.fit(df)

    scored = df.copy()
    scored["uplift_score"] = model.predict_uplift(df)
    scored["uplift_decile"] = pd.qcut(
        scored["uplift_score"],
        q=10,
        labels=False,
        duplicates="drop",
    )
    scored["uplift_decile"] = scored["uplift_decile"].astype(int) + 1

    deciles = (
        scored.groupby("uplift_decile", as_index=False)
        .agg(
            avg_uplift=("uplift_score", "mean"),
            users=("user_id", "count"),
            conversion_rate=("converted", "mean"),
        )
        .sort_values("uplift_decile")
    )
    return deciles


def main() -> None:
    st.title("ML A/B Testing Command Center")
    st.caption("Real-world checkout experiment analytics with statistical guardrails and uplift modeling")

    if st.button("Refresh outputs"):
        st.cache_data.clear()
        st.rerun()

    outcome_path = PROJECT_ROOT / "outputs" / "experiment_outcome.json"
    outcome = load_outcome_json(str(outcome_path))

    if outcome is None:
        st.warning("No experiment outcome found. Run AB_Testing/ab_pipeline.py first.")
        st.stop()

    data_path = Path(outcome["config"]["data_path"])
    df = load_dataset(str(data_path))

    if df.empty:
        st.warning("Dataset is empty or not found. Run the pipeline to generate data.")
        st.stop()

    conversion = outcome["conversion_result"]
    revenue = outcome["revenue_result"]
    validation = outcome["validation"]
    segment = outcome["segment_recommendation"]

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Decision", outcome["decision"])
    col2.metric("Conv. uplift", f"{conversion['uplift']:.2%}")
    col3.metric("Revenue uplift", f"{revenue['uplift']:.3f}")
    col4.metric("SRM p-value", f"{validation['srm_p_value']:.4f}")

    st.subheader("Primary Experiment Metrics")
    metric_table = pd.DataFrame(
        [
            {
                "Metric": "Conversion rate",
                "Control": conversion["control_mean"],
                "Treatment": conversion["treatment_mean"],
                "Uplift": conversion["uplift"],
                "p-value": conversion["p_value"],
                "Significant": conversion["is_significant"],
            },
            {
                "Metric": "Revenue per user (CUPED)",
                "Control": revenue["control_mean"],
                "Treatment": revenue["treatment_mean"],
                "Uplift": revenue["uplift"],
                "p-value": revenue["p_value"],
                "Significant": revenue["is_significant"],
            },
        ]
    )
    st.dataframe(metric_table, use_container_width=True)

    variant_summary = (
        df.groupby("variant", as_index=False)
        .agg(
            users=("user_id", "count"),
            conversion_rate=("converted", "mean"),
            avg_revenue=("revenue", "mean"),
        )
        .sort_values("variant")
    )

    left, right = st.columns(2)
    with left:
        st.subheader("Conversion by Variant")
        st.bar_chart(variant_summary.set_index("variant")["conversion_rate"])
    with right:
        st.subheader("Average Revenue by Variant")
        st.bar_chart(variant_summary.set_index("variant")["avg_revenue"])

    st.subheader("Uplift Targeting")
    st.write(
        f"Recommended segment: {segment['segment_name']} | "
        f"Users: {segment['size']} | "
        f"Avg predicted uplift: {segment['avg_uplift']:.2%} | "
        f"Expected incremental conversions: {segment['expected_incremental_conversions']:.2f}"
    )

    seed = int(outcome["config"]["seed"])
    deciles = compute_uplift_deciles(df, seed)
    st.line_chart(deciles.set_index("uplift_decile")["avg_uplift"])
    st.dataframe(deciles, use_container_width=True)


if __name__ == "__main__":
    main()
