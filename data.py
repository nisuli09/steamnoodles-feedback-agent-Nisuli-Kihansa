
from __future__ import annotations
import pandas as pd
from pathlib import Path

REQUIRED_COLS = ["review_text", "timestamp"]

def load_reviews(csv_path: str | Path) -> pd.DataFrame:
    csv_path = Path(csv_path)
    if not csv_path.exists():
        raise FileNotFoundError(f"CSV not found: {csv_path}")
    df = pd.read_csv(csv_path)
    for col in REQUIRED_COLS:
        if col not in df.columns:
            raise ValueError(f"Missing required column: {col}")
    # Normalize columns
    df = df.copy()
    df["review_text"] = df["review_text"].astype(str).fillna("")
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
    df = df.dropna(subset=["timestamp"]).reset_index(drop=True)
    # optional sentiment column
    if "sentiment" in df.columns:
        df["sentiment"] = df["sentiment"].str.lower().str.strip()
    return df
