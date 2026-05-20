# Usage Examples

All examples use the same `get_ohlc` function — only the broker, symbol, interval, and date range change.

## Save Data to CSV, Excel, or Parquet

```python
from pricehub import get_ohlc

df = get_ohlc("binance_spot", "BTCUSDT", "1d", "2024-10-01", "2024-10-05")
df.to_csv("btcusdt_1d.csv")
df.to_excel("btcusdt_1d.xlsx")
df.to_parquet("btcusdt_1d.parquet")  # requires pyarrow or fastparquet
```

## Binance Spot — 6-Hour Interval

```python
from pricehub import get_ohlc

df = get_ohlc(
    broker="binance_spot",
    symbol="BTCUSDT",
    interval="6h",
    start="2024-10-01",
    end="2024-10-02",
)
print(df)
```

The returned DataFrame includes all fields from the official API: `Open`, `High`, `Low`, `Close`, `Volume`, `Close time`, `Quote asset volume`, `Number of trades`, `Taker buy base asset volume`, `Taker buy quote asset volume`.

## Bybit Spot — 1-Day Interval with Unix Timestamps

```python
from pricehub import get_ohlc

df = get_ohlc(
    broker="bybit_spot",
    symbol="ETHUSDT",
    interval="1d",
    start=1727740800.0,    # Unix seconds
    end=1728086400000,     # Unix milliseconds
)
print(df)
```

PriceHub accepts timestamps in any common format: seconds, milliseconds, ISO 8601 strings, `datetime`, `pandas.Timestamp`, or `arrow.Arrow`.

## KuCoin Spot — 1-Hour Interval

```python
from pricehub import get_ohlc

df = get_ohlc(
    broker="kucoin_spot",
    symbol="BTC-USDT",
    interval="1h",
    start="2024-12-01",
    end="2024-12-02",
)
```

Note KuCoin uses dash-separated symbols (`BTC-USDT`).

## Bitget Spot — 1-Day Interval

```python
from pricehub import get_ohlc

df = get_ohlc(
    broker="bitget_spot",
    symbol="BTCUSDT",
    interval="1d",
    start="2024-12-01",
    end="2024-12-05",
)
```

Returned columns: `Open`, `High`, `Low`, `Close`, `Volume`, `Quote volume`, `USDT volume`.

## Bitget Futures (USDT-M Perpetual) — 1-Hour Interval

```python
from pricehub import get_ohlc

df = get_ohlc(
    broker="bitget_futures",
    symbol="BTCUSDT",
    interval="1h",
    start="2024-12-01",
    end="2024-12-02",
)
```

`bitget_futures` fetches USDT-margined perpetual swaps from Bitget's historical futures endpoint. Returned columns: `Open`, `High`, `Low`, `Close`, `Volume`, `Quote volume`.

## KuCoin Futures — 1-Hour Interval

```python
from pricehub import get_ohlc

df = get_ohlc(
    broker="kucoin_futures",
    symbol="XBTUSDTM",
    interval="1h",
    start="2024-12-01",
    end="2024-12-02",
)
```

## Plot Daily Close — Binance Futures (Last Year)

```python
import matplotlib.pyplot as plt
from pricehub import get_ohlc

df = get_ohlc("binance_futures", "BTCUSDT", "1d", "2023-11-01", "2024-11-01")
df["Close"].plot(figsize=(12, 5), title="BTCUSDT Futures — Daily Close")
plt.show()
```

## Plot Weekly Candlestick — Binance Spot (5 Years)

```python
import plotly.graph_objects as go
from pricehub import get_ohlc

df = get_ohlc("binance_spot", "BTCUSDT", "1w", "2019-11-01", "2024-11-01")
fig = go.Figure(go.Candlestick(
    x=df.index, open=df["Open"], high=df["High"], low=df["Low"], close=df["Close"]
))
fig.update_layout(title="BTCUSDT Spot — Weekly OHLC")
fig.show()
```

## Custom Intervals (e.g., 10 Minutes)

When an exchange doesn't natively support an interval, fetch a finer granularity and resample:

```python
from pricehub import get_ohlc

df = get_ohlc("bybit_spot", "SOLUSDT", "5m", "2024-10-01", "2024-11-01")

df_10m = df.resample("10min").agg({
    "Open": "first",
    "High": "max",
    "Low": "min",
    "Close": "last",
    "Volume": "sum",
})
```

## Supported Intervals

Depends on the broker. Common across most exchanges:

- **Seconds**: `1s` (limited support)
- **Minutes**: `1m`, `3m`, `5m`, `15m`, `30m`
- **Hours**: `1h`, `2h`, `4h`, `6h`, `12h`
- **Days**: `1d`, `3d`
- **Weeks**: `1w`
- **Months**: `1M`
