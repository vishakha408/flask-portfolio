import yfinance as yf


def get_stock_data(ticker, period="1y"):
    ticker = ticker.upper().strip()
    stock = yf.Ticker(ticker)

    prices = stock.history(period=period)
    if prices.empty:
        raise ValueError("Price data unavailable")

    # --- Company name: try multiple yfinance attributes ---
    name = "Unknown"
    try:
        # yfinance v0.2+ exposes fast_info which is more reliable than stock.info
        fast = stock.fast_info
        name = getattr(fast, "display_name", None) or getattr(fast, "short_name", None) or "Unknown"
    except Exception:
        pass

    if name == "Unknown":
        # Fallback: try stock.info (slower, may fail on some versions)
        try:
            info = stock.info or {}
            name = (
                info.get("shortName")
                or info.get("longName")
                or "Unknown"
            )
        except Exception:
            pass

    # --- Financials ---
    try:
        financials = stock.financials
        if financials is not None and financials.empty:
            financials = None
    except Exception:
        financials = None

    # --- Balance sheet ---
    try:
        balance = stock.balance_sheet
        if balance is not None and balance.empty:
            balance = None
    except Exception:
        balance = None

    # --- Full info dict (best-effort, for any extra fields) ---
    try:
        info = stock.info or {}
    except Exception:
        info = {}

    return {
        "ticker": ticker,
        "name": name,
        "prices": prices,
        "financials": financials,
        "balance": balance,
        "info": info,
    }
