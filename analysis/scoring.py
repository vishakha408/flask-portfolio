import numpy as np

def safe_score(value, thresholds):
    """
    thresholds: list of (limit, score) sorted high → low
    """
    if value is None:
        return 0

    for limit, score in thresholds:
        if value >= limit:
            return score

    return 0


# Fundamental Scores

def score_revenue_growth(growth):
    return safe_score(growth, [
        # limit, score pairs for revenue growth with higher growth rates receiving higher scores
        (15, 10),
        (8, 7),
        (0, 5),
        (-np.inf, 2)
    ])


def score_profit_margin(margin):
    return safe_score(margin, [
        # limit, score pairs for profit margin with higher margins receiving higher scores
        (20, 10),
        (10, 7),
        (5, 5),
        (-np.inf, 2)
    ])


def score_roe(roe):
    return safe_score(roe, [
         # limit, score pairs for return on equity with higher ROE values receiving higher scores
        (20, 10),
        (15, 7),
        (10, 5),
        (-np.inf, 2)
    ])


def score_debt_to_equity(dte):
    # scoring for debt to equity ratio with lower ratios receiving higher scores, as they indicate less financial risk
    if dte is None:
        return 0
    if dte < 0.5:
        return 10
    elif dte < 1:
        return 7
    elif dte < 2:
        return 5
    return 2


# Technical Scores

def score_rsi(rsi_value):
    # scoring for relative strength index (RSI) with lower RSI values receiving higher scores,
    # as they may indicate oversold conditions and potential buying opportunities
    if rsi_value is None:
        return 0
    if rsi_value < 30:
        return 8
    elif rsi_value < 70:
        return 6
    return 3


def score_macd(macd, signal):
    # scoring for moving average convergence divergence (MACD) with higher MACD values relative to the signal line receiving higher scores,
    # as they may indicate bullish momentum and potential buying opportunities
    if macd is None or signal is None:
        return 0
    if macd > signal:
        return 8
    else:
        return 4


# Aggregation
def overall_score(fundamental_score, technical_score, weights=None):
    if not weights:
        weights = {
            "fundamentals": 0.6,
            "technicals": 0.4
        }
    # the weights dictionary can be passed as an argument to function, and if the caller does not provide the weights
    # or if they provide a weights dictionary wiht missing one of the keys, it still works correctly
    f = weights.get("fundamentals", 0.6)
    t = weights.get("technicals", 0.4)

    #individual scoring functions is averaged in file app.py
    return round(fundamental_score * f + technical_score * t, 2)

def recommendation(score):
    # the recommendation function provides a simple recommendation based on the overall score,
    # we calculate the scores based on positive indicators for buying the stock, strong fundamentals and bullish technical signals,
    # not for selling the stock. Therefore, lower score would indicate a weaker buy recommendation or a hold/sell recommendation.
    if score >= 7.5:
        return "BUY"
    elif score >= 5.5:
        return "HOLD"
    return "SELL"
