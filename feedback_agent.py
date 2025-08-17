
from __future__ import annotations
from dataclasses import dataclass
from utils.llm import classify_and_reply, Sentiment

@dataclass
class FeedbackResult:
    sentiment: Sentiment
    reply: str

class FeedbackAgent:
    def __init__(self, brand_name: str = "SteamNoodles") -> None:
        self.brand_name = brand_name

    def run(self, review_text: str) -> FeedbackResult:
        sentiment, reply = classify_and_reply(review_text, brand_name=self.brand_name)
        return FeedbackResult(sentiment=sentiment, reply=reply)
