import time
 
import yfinance as yf
 
 
def get_stock_data(ticker, period="1y"):
    ticker = ticker.upper().strip()
 
    # Use a real browser User-Agent so Yahoo doesn't block Render's servers 
    session = None
    try:
        import requests
        session = requests.Session()
        session.headers.update({
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            )
        })
    except Exception:
        pass
 
    ticker = ticker.upper().strip()
    stock = yf.Ticker(ticker, session=session)

    #  Price history (retry 3×)
    prices = None
    for attempt in range(3):
        try:
            prices = stock.history(period=period, auto_adjust=True)
            if prices is not None and not prices.empty:
                break
        except Exception as exc:
            print(f"[data] price fetch attempt {attempt + 1} failed: {exc}")
        time.sleep(1)

    if prices is None or prices.empty:
        raise ValueError(f"Price data unavailable for '{ticker}'. "
                         "Check that the ticker symbol is correct.")

    # Company name
    # fast_info does NOT reliably expose display_name/short_name across all
    # yfinance versions — use stock.info instead (one HTTP call, cached by yf).
    name = "Unknown"
    try:
        info = stock.info or {}
        name = (
            info.get("shortName")
            or info.get("longName")
            or info.get("name")
            or "Unknown"
        )
    except Exception as exc:
        print(f"[data] could not fetch company name: {exc}")

    # Financials
    financials = None
    try:
        df = stock.financials
        if df is not None and not df.empty:
            financials = df
    except Exception as exc:
        print(f"[data] financials fetch failed: {exc}")

    # Balance sheet
    balance = None
    try:
        df = stock.balance_sheet
        if df is not None and not df.empty:
            balance = df
    except Exception as exc:
        print(f"[data] balance sheet fetch failed: {exc}")

    # Full info dict
    try:
        info = stock.info or {}
    except Exception:
        info = {}

    return {
        "ticker":     ticker,
        "name":       name,
        "prices":     prices,
        "financials": financials,
        "balance":    balance,
        "info":       info,
    }
