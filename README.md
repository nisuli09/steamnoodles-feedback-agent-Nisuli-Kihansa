
# SteamNoodles – Automated Restaurant Feedback Agents

A minimal, production-ready sample project implementing **two AI agents** with **LangChain**:

- **Agent 1 – Feedback Response Agent**: Classifies sentiment of a single review (positive/negative/neutral) and generates a short, polite, context-aware reply.
- **Agent 2 – Sentiment Visualization Agent**: Given a date range (e.g., `"last 7 days"` or `"2025-06-01 to 2025-06-15"`), creates a **daily bar/line chart** for positive/neutral/negative review counts.




# Quickstart

1) **Python** 

2) **Install**:
bash
pip install -r requirements.txt


3) **Set API key** 


4) **Data**: 
- review_text – the raw customer review text
- timestamp – parseable date/time (e.g., '2025-06-03 14:10:00')
- Optional - sentiment – one of 'positive', 'negative', 'neutral'

 **sample dataset** 

5) **Run Agent 1** (single review -> auto-reply):
bash
python main.py reply --text "The noodles were fantastic but service was slow."


6) **Run Agent 2** (plot date range):
bash
# last 7 days
python main.py plot --range "last 7 days"


python main.py plot --range "2025-06-01 to 2025-06-15"





# K.A. Nisuli Kihansa
# NSBM Green University - 3rd year 



