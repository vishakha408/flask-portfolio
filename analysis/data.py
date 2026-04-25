import yfinance as yf


def get_stock_data(ticker, period="1y"):
    ticker = ticker.upper().strip()
    stock = yf.Ticker(ticker)

    prices = stock.history(period=period)
    if prices.empty:
        raise ValueError("Price data unavailable")

    # --- Company name: try methods in order of reliability ---
    name = "Unknown"

    # Method 1: history_metadata (comes free with history(), no extra request)
    try:
        meta = stock.get_history_metadata()
        name = (
            meta.get("shortName")
            or meta.get("longName")
            or meta.get("symbol")
            or "Unknown"
        )
    except Exception:
        pass

    # Method 2: basic_info (lightweight, doesn't hit quoteSummary endpoint)
    if name == "Unknown":
        try:
            bi = stock.basic_info
            name = (
                getattr(bi, "short_name", None)
                or getattr(bi, "long_name", None)
                or "Unknown"
            )
        except Exception:
            pass

    # Method 3: full info as last resort
    if name == "Unknown":
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

    # --- Full info dict (best-effort) ---
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
