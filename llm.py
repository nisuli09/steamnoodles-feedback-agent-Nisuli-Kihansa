
from __future__ import annotations
from typing import Literal, Tuple
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

Sentiment = Literal["positive","negative","neutral"]

def get_llm(model: str = "gpt-4o-mini", temperature: float = 0.2):
    """Configure the chat LLM (OpenAI by default)."""
    return ChatOpenAI(model=model, temperature=temperature)

def classify_and_reply(review_text: str, brand_name: str = "SteamNoodles") -> Tuple[Sentiment, str]:
    """Use the LLM to classify sentiment and generate a short, polite reply."""
    system = (
        "You are a customer support assistant for a restaurant. "
        "Classify sentiment (positive/negative/neutral) and write a concise, empathetic reply. "
        "If issues are mentioned, apologize and promise to improve. Always include the brand name when signing off."
    )
    user = (
        "Classify the sentiment of this review as one word (positive/negative/neutral), "
        "then write a brief (<=60 words) reply.\n\nReview: {review_text}\n\n"
        "Return JSON with keys: sentiment, reply."
    )
    prompt = ChatPromptTemplate.from_messages([("system", system), ("user", user)])
    chain = prompt | get_llm()  # returns an AIMessage
    ai_message = chain.invoke({"review_text": review_text})
    content = ai_message.content
    # Try to extract JSON; if not strict JSON, attempt a fallback parse.
    import json, re
    try:
        data = json.loads(content)
    except Exception:
        # naive extraction
        m = re.search(r"\{[\s\S]*\}", content)
        if m:
            data = json.loads(m.group(0))
        else:
            # final fallback
            data = {"sentiment": "neutral", "reply": content.strip()[:300]}
    sentiment = str(data.get("sentiment", "neutral")).lower()
    if sentiment not in {"positive","negative","neutral"}:
        sentiment = "neutral"
    reply = str(data.get("reply", "Thank you for your feedback. — "+brand_name)).strip()
    return sentiment, reply
