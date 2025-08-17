
# SteamNoodles – Automated Restaurant Feedback Agents

A minimal, production-ready sample project implementing **two AI agents** with **LangChain**:

- **Agent 1 – Feedback Response Agent**: Classifies sentiment of a single review (positive/negative/neutral) and generates a short, polite, context-aware reply.
- **Agent 2 – Sentiment Visualization Agent**: Given a date range (e.g., `"last 7 days"` or `"2025-06-01 to 2025-06-15"`), creates a **daily bar/line chart** for positive/neutral/negative review counts.

> Works with any CSV that has columns: `review_text`, `timestamp` (ISO date or parseable), and (optional) `sentiment`.> If `sentiment` is missing, Agent 1 will infer it with the LLM.

---

## Quickstart

1) **Python**: 3.10+ recommended

2) **Install**:
```bash
pip install -r requirements.txt
```

3) **Set API key** (only needed if you use OpenAI or other hosted LLMs):
```bash
# on mac/linux
export OPENAI_API_KEY="sk-yourkey"

# on windows (powershell)
setx OPENAI_API_KEY "sk-yourkey"
```

4) **Data**: Put your CSV at `data/reviews.csv` with columns:
- `review_text` – the raw customer review text
- `timestamp` – parseable date/time (e.g., `2025-06-03 14:10:00`)
- Optional: `sentiment` – one of `positive`, `negative`, `neutral`

A tiny **sample dataset** is already included.

5) **Run Agent 1** (single review -> auto-reply):
```bash
python main.py reply --text "The noodles were fantastic but service was slow."
```

6) **Run Agent 2** (plot date range):
```bash
# last 7 days
python main.py plot --range "last 7 days"

# explicit dates (inclusive)
python main.py plot --range "2025-06-01 to 2025-06-15"
```

Charts are saved to `artifacts/plots/` and filenames include the date range.

---

## Project Structure

```
steamnoodles-agents/
├── agents/
│   ├── feedback_agent.py
│   └── viz_agent.py
├── utils/
│   ├── data.py
│   ├── llm.py
│   └── dateparse.py
├── data/
│   └── reviews.csv
├── notebooks/
│   └── demo.ipynb
├── artifacts/    # created at runtime
├── main.py
├── requirements.txt
└── README.md
```

---

## Notes

- **LLM choice**: default is `openai` via LangChain; switch to `ollama`/`groq`/`huggingface` by editing `utils/llm.py`.
- **No internet?** You can plug in a local model (e.g., `ollama`) in `utils/llm.py`.
- **Reproducibility**: deterministic temperature is set low for short and polite replies.
- **Plotting**: uses **matplotlib** only.

---

## License
MIT
