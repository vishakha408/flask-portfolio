import yfinance as yf


def get_stock_data(ticker, period="1y"):
    ticker = ticker.upper().strip()
    stock = yf.Ticker(ticker)

    prices = stock.history(period=period)
    if prices.empty:
        raise ValueError("Price data unavailable")

    # --- Company name: try multiple yfinance attributes ---
    name = None
    try:
        fast = stock.fast_info
        name = getattr(fast, "display_name", None) or getattr(fast, "short_name", None)
    except Exception:
        pass

    if not name:
        try:
            info = stock.info or {}
            name = info.get("shortName") or info.get("longName")
        except Exception:
            pass

    if not name:
        try:
            meta = stock.get_history_metadata()
            name = meta.get("shortName") or meta.get("longName")
        except Exception:
            pass

    # Last resort: just show the ticker symbol instead of "Unknown"
    name = name or ticker

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
