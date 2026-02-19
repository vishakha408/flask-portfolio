import yfinance as yf

def get_stock_data(ticker, period="1y"):
    ticker = ticker.upper().strip()
    stock = yf.Ticker(ticker)

    prices = stock.history(period=period)
    if prices.empty:
        raise ValueError("Price data unavailable")

    # Info (slow / unreliable)
    try:
        info = stock.info or {}
    except Exception:
        info = {}

    # Financials
    try:
        financials = stock.financials
    except Exception:
        financials = None

    # Balance sheet
    try:
        balance = stock.balance_sheet
    except Exception:
        balance = None

    return {
        "ticker": ticker,
        "name": info.get("shortName", "Unknown"),
        "prices": prices,
        "financials": financials,
        "balance": balance,
        "info": info,
    }
