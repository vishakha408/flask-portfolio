import pandas as pd


def rsi(price_df, period=14):
    if price_df is None or price_df.empty:
        return None

    if "Close" not in price_df.columns:
        return None

    if len(price_df) < period + 1:
        return None
    #.diff() calculates the difference between the current and previous closing price, giving us the daily change in price.
    delta = price_df["Close"].diff()

    #gain and loss are dataframes that contain the positive and negative changes in price, respectively.
    #.where(delta > 0, 0) means that if the condition (delta > 0) is true,
    # it keeps the original value of delta; otherwise, it replaces it with 0.
    gain = delta.where(delta > 0, 0)

    # The negative values in loss are negated to make them positive.
    loss = -delta.where(delta < 0, 0)

    #.rolling(period).mean() calculates the rolling average of the gain and loss over the specified period (default is 14 days).
    avg_gain = gain.rolling(period).mean()
    avg_loss = loss.rolling(period).mean()


    last_loss = avg_loss.iloc[-1]
    if pd.isna(last_loss) or last_loss == 0:
        return None
    rs = avg_gain / avg_loss
    rsi_value = 100 - (100 / (1 + rs))

    #rs and rsi_value conatins multiple values but we are interested in the last value which is the most recent RSI value.
    # Hence we take rsi_value.iloc[-1] to get the latest RSI value.
    return round(rsi_value.iloc[-1], 2)

def ema(value, period):
        #Formula: EMA = (Price × k) + (Previous EMA × (1 − k) Where: k = 2 / (n + 1)
        k = 2 / (period + 1)
        ema_values = [value[0]]  # start EMA at first price

        for i in range(1, len(value)):
           ema_today = value[i] * k + ema_values[-1] * (1 - k)
           ema_values.append(ema_today)

        return ema_values

def macd(price_df):
    if price_df is None or price_df.empty:
        return None

    if "Close" not in price_df.columns:
        return None

    if len(price_df) < 26:
        return None

    # Convert to plain Python list
    close = price_df["Close"].tolist()

    exp12 = ema(close, 12)
    exp26 = ema(close, 26)

    # MACD line
    macd_line = []
    for i in range(len(close)):
        macd_line.append(exp12[i] - exp26[i])

    # Signal line
    signal_line = ema(macd_line, 9)

    # Histogram
    histogram = []
    for i in range(len(macd_line)):
        histogram.append(macd_line[i] - signal_line[i])

    # Return LAST values only
    return {
        "macd": round(macd_line[-1], 2),
        "signal": round(signal_line[-1], 2),
        "histogram": round(histogram[-1], 2),
    }


#simple moving average
def moving_averages(price_df):
    if price_df is None or price_df.empty:
        return None

    if "Close" not in price_df.columns:
        return None

    df = price_df.copy()

    if len(df) < 50:
        return None
    #df is updated with two new columns, "MA_50" and "MA_200"
    df["MA_50"] = df["Close"].rolling(50).mean()
    df["MA_200"] = df["Close"].rolling(200).mean()

    # The latest values of the 50-day and 200-day moving averages
    ma_50 = df["MA_50"].iloc[-1]
    ma_200 = df["MA_200"].iloc[-1]

    return {
        "ma_50": round(ma_50, 2) if not pd.isna(ma_50) else None,
        "ma_200": round(ma_200, 2) if not pd.isna(ma_200) else None,
    }
