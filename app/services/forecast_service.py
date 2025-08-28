import pandas as pd
from sklearn.linear_model import LinearRegression

def forecast_sales(data: list, date_col: str = "OrderDate", value_col: str = "LineTotal", periods: int = 1):
    if not data:
        return {"forecast": [], "note": "No data to forecast"}

    df = pd.DataFrame(data)
    df[date_col] = pd.to_datetime(df[date_col])

    monthly = df.groupby(df[date_col].dt.to_period("M"))[value_col].sum().reset_index()
    monthly[date_col] = monthly[date_col].dt.to_timestamp()

    monthly["t"] = range(len(monthly))
    X = monthly[["t"]]
    y = monthly[value_col]

    model = LinearRegression()
    model.fit(X, y)

    future_t = list(range(len(monthly), len(monthly) + periods))
    future_dates = [monthly[date_col].iloc[-1] + pd.DateOffset(months=i+1) for i in range(periods)]
    predictions = model.predict(pd.DataFrame({"t": future_t}))

    forecast = [{"date": d.strftime("%Y-%m"), "predicted_sales": round(float(p), 2)}
                for d, p in zip(future_dates, predictions)]

    return {"forecast": forecast, "note": "Linear regression on monthly sales"}
