def revenue_growth(financials):
    if financials is None or financials.empty:
        return None

    if "Total Revenue" not in financials.index:
        return None

    revenue = financials.loc["Total Revenue"]

    #If there is only one value- IndexError or ZeroDivisionError
    if len(revenue) < 2 or revenue.iloc[1] == 0:
        return None

    growth = (revenue.iloc[0] - revenue.iloc[1]) / revenue.iloc[1]
    return round(growth * 100, 2)


def net_profit_margin(financials):
    if financials is None or financials.empty:
        return None

    if "Net Income" not in financials.index or "Total Revenue" not in financials.index:
        return None

    revenue = financials.loc["Total Revenue"].iloc[0]
    if revenue == 0:
        return None

    net_income = financials.loc["Net Income"].iloc[0]
    return round((net_income / revenue) * 100, 2)


def return_on_equity(financials, balance_sheet):
    if financials is None or financials.empty:
        return None
    if balance_sheet is None or balance_sheet.empty:
        return None

    if "Net Income" not in financials.index:
        return None

    equity_keys = [
        "Total Stockholder Equity",
        "Stockholders Equity"
    ]

    equity = None
    for key in equity_keys:
        if key in balance_sheet.index:
            equity = balance_sheet.loc[key].iloc[0]
            break

    if equity in (None, 0):
        return None

    net_income = financials.loc["Net Income"].iloc[0]
    return round((net_income / equity) * 100, 2)


def debt_to_equity(balance_sheet):
    if balance_sheet is None or balance_sheet.empty:
        return None

    if "Total Debt" not in balance_sheet.index:
        return None

    equity_keys = [
        "Total Stockholder Equity",
        "Stockholders Equity"
    ]

    equity = None
    for key in equity_keys:
        if key in balance_sheet.index:
            equity = balance_sheet.loc[key].iloc[0]
            break

    if equity in (None, 0):
        return None

    total_debt = balance_sheet.loc["Total Debt"].iloc[0]
    return round(total_debt / equity, 2)
