from dotenv import load_dotenv
load_dotenv()

from flask import Flask, render_template, request
from flask_caching import Cache

from ai_summary import generate_summary
from analysis import data, fundamentals, technicals, scoring, charts

app = Flask(__name__)

# Cache
cache = Cache(app, config={
    "CACHE_TYPE": "SimpleCache",
    "CACHE_DEFAULT_TIMEOUT": 900,
})


@cache.memoize(timeout=900)
def get_cached_stock_data(ticker):
    return data.get_stock_data(ticker)


#  Core analysis
def analyze_stock(ticker):
    ticker     = ticker.upper()
    stock_data = get_cached_stock_data(ticker)

    prices     = stock_data["prices"]
    financials = stock_data.get("financials")
    balance    = stock_data.get("balance")
    name       = stock_data["name"]

    if prices is None or prices.empty:
        raise ValueError("Price data unavailable")

    # Fundamentals
    fundamentals_data  = {}
    fundamental_score  = 0

    if (financials is not None and not financials.empty
            and balance is not None and not balance.empty):
        try:
            fundamentals_data = {
                "revenue_growth": fundamentals.revenue_growth(financials),
                "profit_margin":  fundamentals.net_profit_margin(financials),
                "roe":            fundamentals.return_on_equity(financials, balance),
                "debt_to_equity": fundamentals.debt_to_equity(balance),
            }
            fundamental_score = sum([
                scoring.score_revenue_growth(fundamentals_data["revenue_growth"]),
                scoring.score_profit_margin(fundamentals_data["profit_margin"]),
                scoring.score_roe(fundamentals_data["roe"]),
                scoring.score_debt_to_equity(fundamentals_data["debt_to_equity"]),
            ]) / 4
        except Exception as exc:
            print(f"[app] Fundamentals calculation error: {exc}")
            fundamentals_data = {}
            fundamental_score = 0

    # Technicals
    rsi_value = technicals.rsi(prices)

    macd_data = technicals.macd(prices)
    if macd_data is None:
        macd_data = {"macd": None, "signal": None, "histogram": None}

    technical_score = (
        scoring.score_rsi(rsi_value) +
        scoring.score_macd(macd_data["macd"], macd_data["signal"])
    ) / 2

    total_score    = scoring.overall_score(fundamental_score, technical_score)
    recommendation = scoring.recommendation(total_score)

    #Charts
    charts_data = {}
    try:
        charts_data = {
            "rsi":  charts.plot_rsi(prices, ticker),
            "macd": charts.plot_macd(prices, ticker),
        }
    except Exception as exc:
        print(f"[app] Chart error: {exc}")

    # AI Summary
    technicals_data = {"rsi": rsi_value, "macd": macd_data}

    ai_summary = generate_summary(
        ticker         = ticker,
        name           = name,
        score          = total_score,
        recommendation = recommendation,
        fundamentals   = fundamentals_data,
        technicals     = technicals_data,
    )

    if ai_summary is None:
        print("[app] WARNING: AI summary returned None. "
              "Check that GEMINI_API_KEY is set and valid.")

    return {
        "ticker":         ticker,
        "name":           name,
        "score":          total_score,
        "recommendation": recommendation,
        "fundamentals":   fundamentals_data,
        "technicals": {
            "rsi":  rsi_value,
            "macd": macd_data,
        },
        "charts":    charts_data,
        "ai_summary": ai_summary,
    }


# Routes
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        ticker = request.form.get("ticker", "").strip()

        if not ticker:
            return render_template("index.html",
                                   error="Please enter a ticker symbol.")
        try:
            result = analyze_stock(ticker)
            return render_template("result.html", result=result)
        except Exception as exc:
            print(f"[app] ERROR: {exc}")
            return render_template("index.html",
                                   error="Invalid ticker or data unavailable. "
                                         "Please check the symbol and try again.")

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
