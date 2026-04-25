from flask import Flask, render_template, request, jsonify
from flask_caching import Cache

from analysis import data, fundamentals, technicals, scoring, charts

app = Flask(__name__)

# ---- Cache ----

cache = Cache(app, config={
    "CACHE_TYPE": "SimpleCache",
    # Caching stock data for 15 minutes
    "CACHE_DEFAULT_TIMEOUT": 900
})

@cache.memoize(timeout=900)
def get_cached_stock_data(ticker):
    return data.get_stock_data(ticker)

# Core analysis
def analyze_stock(ticker):
    ticker = ticker.upper()
    stock_data = get_cached_stock_data(ticker)

    prices = stock_data["prices"]
    financials = stock_data.get("financials")
    balance = stock_data.get("balance")
    name = stock_data["name"]

    if prices is None or prices.empty:
        raise ValueError("Price data unavailable")

    # Fundamentals
    fundamentals_data = {}
    fundamental_score = 0

    if financials is not None and not financials.empty and balance is not None and not balance.empty:
        fundamentals_data = {
            "revenue_growth": fundamentals.revenue_growth(financials),
            "profit_margin": fundamentals.net_profit_margin(financials),
            "roe": fundamentals.return_on_equity(financials, balance),
            "debt_to_equity": fundamentals.debt_to_equity(balance),
        }

        fundamental_score = sum([
            scoring.score_revenue_growth(fundamentals_data["revenue_growth"]),
            scoring.score_profit_margin(fundamentals_data["profit_margin"]),
            scoring.score_roe(fundamentals_data["roe"]),
            scoring.score_debt_to_equity(fundamentals_data["debt_to_equity"]),
        ]) / 4

    # Technicals
    rsi_value = technicals.rsi(prices)

    # FIX: macd() can return None if not enough data — guard before subscripting
    macd_data = technicals.macd(prices)
    if macd_data is None:
        macd_data = {"macd": None, "signal": None, "histogram": None}

    technical_score = (
        scoring.score_rsi(rsi_value) +
        scoring.score_macd(macd_data["macd"], macd_data["signal"])
    ) / 2

    total_score = scoring.overall_score(fundamental_score, technical_score)

    # Charts
    charts_data = {}
    try:
        charts_data = {
            "rsi": charts.plot_rsi(prices, ticker),
            "macd": charts.plot_macd(prices, ticker),
        }
    except Exception as e:
        print("Chart error:", e)

    return {
        "ticker": ticker,
        "name": name,
        "score": total_score,
        "recommendation": scoring.recommendation(total_score),
        "fundamentals": fundamentals_data,
        "technicals": {
            "rsi": rsi_value,
            "macd": macd_data,
        },
        "charts": charts_data,
    }


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        ticker = request.form.get("ticker", "").strip()

        if not ticker:
            return render_template("index.html", error="Please enter a ticker symbol.")
        try:
            result = analyze_stock(ticker)
            return render_template("result.html", result=result)
        except Exception as e:
            print("ERROR:", e)
            return render_template("index.html", error="Invalid ticker or data unavailable.")

    return render_template("index.html")


if __name__ == "__main__":
    app.run()
