import os
import matplotlib.pyplot as plt
from analysis.technicals import ema

# Base directory of this file
# __file__ contains the path of the current file i.e. charts.py.
# os.path.abspath(__file__) gives the absolute path of charts.py  like C:/Users/VISHAKHA/Desktop/stock-analyzer/analysis/charts.py
# os.path.dirname() extracts the base directory where charts.py is located i.e. C:/Users/VISHAKHA/Desktop/stock-analyzer/analysis
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Static folder path for saving charts
#.. moves one level up to C:/Users/VISHAKHA/Desktop/stock-analyzer and then adds "static"
# to get C:/Users/VISHAKHA/Desktop/stock-analyzer/static
STATIC_DIR = os.path.join(BASE_DIR, "..", "static")


def plot_rsi(prices, ticker, period=14):
    if prices is None or prices.empty or "Close" not in prices.columns:
        return None

    if len(prices) < period + 1:
        return None

    delta = prices["Close"].diff()

    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)

    avg_gain = gain.rolling(period).mean()
    avg_loss = loss.rolling(period).mean()

    #zero division check for avg_loss
    last_loss = avg_loss.iloc[-1]
    # last_loss != last_loss is a check for NaN values, as NaN is not equal to itself in Python.
    # This condition ensures that if last_loss is NaN, the function will return None instead of calculating
    if last_loss != last_loss or last_loss == 0:
        return None

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))

    # Create static directory if missing
    # This ensures that the directory "static" exists before trying to save the chart
    os.makedirs(STATIC_DIR, exist_ok=True)

    # File path for RSI chart
    # creating a file path like C:/Users/VISHAKHA/Desktop/stock-analyzer/static/AAPL_rsi.png
    path = os.path.join(STATIC_DIR, f"{ticker}_rsi.png")

    plt.figure(figsize=(8, 4))
    plt.plot(rsi, label="RSI")
    plt.axhline(30, linestyle="--", alpha=0.6)
    plt.axhline(70, linestyle="--", alpha=0.6)
    plt.title(f"{ticker} RSI")
    plt.legend()
    plt.tight_layout()

    #The plt.savefig(path) line saves the current figure to the specified path as an image file (in this case, a PNG).
    plt.savefig(path)
    
    # The plt.close() line then closes the figure to free up memory. The function returns the filename of the saved image
    # which is used in the web application to display the chart.
    plt.close()

    return f"{ticker}_rsi.png"

def plot_macd(prices, ticker):
    if prices is None or prices.empty or "Close" not in prices.columns:
        return None

    if len(prices) < 26:
        return None

    # Convert closing prices to list
    close = prices["Close"].tolist()

    # ema
    exp12 = ema(close, 12)
    exp26 = ema(close, 26)

    if exp12 is None or exp26 is None:
        return None

    #MACD line
    macd_line = []
    min_len = min(len(exp12), len(exp26))
    for i in range(min_len):
        macd_line.append(exp12[i] - exp26[i])

    #signal line
    signal_line = ema(macd_line, 9)
    if signal_line is None:
        return None

    # Create static directory if missing
    os.makedirs(STATIC_DIR, exist_ok=True)

    # File path for MACD chart
    path = os.path.join(STATIC_DIR, f"{ticker}_macd.png")


    plt.figure(figsize=(8, 4))
    plt.plot(macd_line, label="MACD")
    plt.plot(signal_line, label="Signal")
    plt.axhline(0, linestyle="--", alpha=0.5)
    plt.legend()
    plt.title(f"{ticker} MACD")
    plt.tight_layout()
    plt.savefig(path)
    plt.close()

    return f"{ticker}_macd.png"

