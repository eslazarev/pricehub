![CI](https://github.com/eslazarev/pricehub/workflows/CI/badge.svg)
![Pylint](https://github.com/eslazarev/pricehub/blob/main/.github/badges/pylint.svg)
![Black](https://img.shields.io/badge/code%20style-black-000000.svg)

# pricehub

**pricehub** is a Python package for retrieving OHLC (Open-High-Low-Close) data across various brokers' APIs with a unified interface. 
It supports multiple markets, including spot and futures, and provides flexible timestamp inputs and a wide range of intervals.

## Key Features

- **Unified Interface**: Supports multiple brokers and markets (spot, futures) with a single interface.
- **Flexible Intervals**: Choose from 1 minute to 1 month intervals.
- **Timestamp Flexibility**: Accepts timestamps in various formats (int, float, string, Arrow, pandas, datetime).
- **No Credential Requirement**: Fetch public market data without authentication.
- **Extended Date Ranges**: Unlike official libraries (e.g., Binance), this package imposes no limit on data retrieval (e.g., 200-day limit bypassed).

### Supported Brokers
- Binance Spot
- Binance Futures
- Bybit Spot

### Supported Intervals
- **Minutes**: `1m`, `3m`, `5m`, `15m`, `30m`
- **Hours**: `1h`, `2h`, `4h`, `6h`, `12h`
- **Days**: `1d`, `3d`
- **Weeks**: `1w`
- **Months**: `1M`

---

## Installation

```bash
pip install pricehub
```

## Quick Start

### Example Usage

#### Retrieve OHLC data from Binance Spot for a 1-hour interval
```python
from pricehub import get_ohlc

df = get_ohlc(
    broker="binance_spot",
    symbol="BTCUSDT",
    interval="1h",
    start="2024-10-01",
    end="2024-10-02"
)
print(df)
```

#### Retrieve OHLC data from Bybit Spot for a 1-day interval
```python
from pricehub import get_ohlc

df = get_ohlc(
    broker="bybit_spot",
    symbol="ETHUSDT",
    interval="1d",
    start="2024-09-01",
    end="2024-09-30"
)
print(df)
```

### API Reference

#### `get_ohlc`

Retrieves OHLC data for the specified broker, symbol, interval, and date range.

- **Parameters**:
  - `broker`: The broker to fetch data from (e.g., `binance_spot`, `bybit_spot`).
  - `symbol`: The trading pair symbol (e.g., `BTCUSDT`).
  - `interval`: The interval for OHLC data (`1m`, `1h`, `1d`, etc.).
  - `start`: Start time of the data (supports various formats).
  - `end`: End time of the data.

- **Returns**:
  - `pandas.DataFrame`: A DataFrame containing OHLC data with `Open time` as the index.

---
