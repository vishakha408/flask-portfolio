import os
from google import genai

_api_key = os.getenv("GEMINI_API_KEY")

if not _api_key:
    print("WARNING: GEMINI_API_KEY is not set — AI summaries will be disabled.")
    _client = None
else:
    _client = genai.Client(api_key=_api_key)

_MODEL = "gemini-2.5-flash"


def generate_summary(ticker, name, score, recommendation, fundamentals, technicals):
    if _client is None:
        return None

    fund = fundamentals or {}
    tech = technicals  or {}
    macd = tech.get("macd") or {}

    prompt = f"""
You are a sharp, experienced buy-side equity analyst writing a brief note for a retail investor.

The investor can already SEE the raw numbers on screen — do NOT restate them.
Your job is to INTERPRET and CONNECT them into actionable insight.

Return exactly 4-5 bullet points using "•" as the bullet character.
Each bullet must be one crisp sentence. Use **bold** for key phrases.
No intro line, no outro line — just the bullets.

Cover these angles (one bullet each):
- What story do the fundamentals tell together? (e.g. is debt justified by ROE? margins vs growth?)
- What is the technical momentum saying? Do RSI and MACD confirm or contradict each other?
- Are fundamentals and technicals aligned or diverging — and what does that mean for timing?
- Biggest risk AND biggest opportunity in one sentence.
- What type of investor is this suited for? (growth / value / momentum / income)

Tone: direct, specific, no fluff. No hedging with "may" or "could".

Data (interpret only — do not repeat these back):
Stock: {name} ({ticker}) | Score: {score}/10 | Signal: {recommendation}
Revenue Growth: {fund.get('revenue_growth', 'N/A')}% | Profit Margin: {fund.get('profit_margin', 'N/A')}% | ROE: {fund.get('roe', 'N/A')}% | Debt/Equity: {fund.get('debt_to_equity', 'N/A')}
RSI: {tech.get('rsi', 'N/A')} | MACD: {macd.get('macd', 'N/A')} | Signal Line: {macd.get('signal', 'N/A')}
""".strip()

    try:
        response = _client.models.generate_content(
            model=_MODEL,
            contents=prompt
        )
        return response.text.strip()

    except Exception as e:
        print(f"[ai_summary] Gemini API error: {e}")
        return None
