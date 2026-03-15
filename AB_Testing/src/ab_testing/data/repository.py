from __future__ import annotations

from pathlib import Path

import pandas as pd

from ab_testing.domain.protocols import ExperimentRepository


class CsvExperimentRepository(ExperimentRepository):
    """Repository adapter to persist experiment datasets as CSV files."""

    def __init__(self, data_path: Path) -> None:
        self._data_path = Path(data_path)

    @property
    def data_path(self) -> Path:
        return self._data_path

    def save(self, df: pd.DataFrame) -> None:
        self._data_path.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(self._data_path, index=False)

    def load(self) -> pd.DataFrame:
        if not self._data_path.exists():
            raise FileNotFoundError(f"Dataset not found at {self._data_path}")
        return pd.read_csv(self._data_path)
