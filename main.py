
from __future__ import annotations
import typer
from agents.feedback_agent import FeedbackAgent
from agents.viz_agent import VizAgent

app = typer.Typer(help="SteamNoodles – Automated Restaurant Feedback Agents")


@app.command()
def reply(text: str):
    """Agent 1: Classify and auto-reply to a single review."""
    agent = FeedbackAgent(brand_name="SteamNoodles")
    res = agent.run(text)
    typer.echo(f"Sentiment: {res.sentiment}")
    typer.echo("Reply:\n" + res.reply)


@app.command()
def plot(range: str = typer.Option(..., "--range", help="Date range, e.g. 'last 7 days' or '2025-06-01 to 2025-06-15'"),
         kind: str = typer.Option("bar", help="'bar' or 'line'")):
    """Agent 2: Generate sentiment visualization for a date range."""
    agent = VizAgent()
    res = agent.run(date_range=range, kind=kind)
    typer.echo(f"Saved plot: {res.out_path}")


if __name__ == "__main__":
    app()
