
from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Tuple
import pandas as pd
import matplotlib.pyplot as plt
from utils.data import load_reviews
from utils.dateparse import parse_range
from utils.llm import classify_and_reply

@dataclass
class VizResult:
    out_path: Path
    start: pd.Timestamp
    end: pd.Timestamp

def ensure_sentiment(df: pd.DataFrame) -> pd.DataFrame:
    """Ensure df has a 'sentiment' column; infer via LLM when missing."""
    if "sentiment" in df.columns and df["sentiment"].notna().all():
        return df
    sentiments = []
    for txt in df["review_text"].tolist():
        s, _ = classify_and_reply(txt)  # reuse classifier; ignore reply
        sentiments.append(s)
    df = df.copy()
    df["sentiment"] = sentiments
    return df

class VizAgent:
    def __init__(self, csv_path: str | Path = "data/reviews.csv", out_dir: str | Path = "artifacts/plots") -> None:
        self.csv_path = Path(csv_path)
        self.out_dir = Path(out_dir)
        self.out_dir.mkdir(parents=True, exist_ok=True)

    def run(self, date_range: str, kind: str = "bar") -> VizResult:
        df = load_reviews(self.csv_path)
        df = ensure_sentiment(df)

        start, end = parse_range(date_range)
        mask = (df["timestamp"] >= start) & (df["timestamp"] <= end)
        dff = df.loc[mask].copy()
        if dff.empty:
            raise ValueError("No reviews in selected date range.")

        dff["date"] = dff["timestamp"].dt.date
        counts = (
            dff.groupby(["date","sentiment"]).size().rename("count").reset_index()
            .pivot(index="date", columns="sentiment", values="count").fillna(0).sort_index()
        )
        # Ensure columns exist
        for col in ["positive","neutral","negative"]:
            if col not in counts.columns:
                counts[col] = 0

        # Plotting with matplotlib (no seaborn)
        plt.figure(figsize=(10,5))
        if kind == "line":
            for col in ["positive","neutral","negative"]:
                plt.plot(counts.index, counts[col], label=col)
        else:
            # stacked bar by default
            bottom = None
            for col in ["positive","neutral","negative"]:
                plt.bar(counts.index, counts[col], bottom=bottom, label=col)
                bottom = (counts[col] if bottom is None else bottom + counts[col])

        plt.legend()
        plt.xlabel("Date")
        plt.ylabel("# Reviews")
        plt.title(f"SteamNoodles Sentiment by Day ({start.date()} to {end.date()})")
        out_name = f"sentiment_{start.date()}_{end.date()}_{kind}.png"
        out_path = self.out_dir / out_name
        plt.tight_layout()
        plt.savefig(out_path)
        plt.close()

        return VizResult(out_path=out_path, start=pd.Timestamp(start), end=pd.Timestamp(end))
