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

```python
                        Open     High      Low    Close      Volume              Close time  Quote asset volume  Number of trades  Taker buy base asset volume  Taker buy quote asset volume  Ignore
Open time                                                                                                                                                                                           
2024-10-01 00:00:00  63309.0  63872.0  63000.0  63733.9   39397.714 2024-10-01 05:59:59.999        2.500830e+09          598784.0                    19410.785                  1.232417e+09     0.0
2024-10-01 06:00:00  63733.9  64092.6  63683.1  63699.9   32857.923 2024-10-01 11:59:59.999        2.100000e+09          446330.0                    15865.753                  1.014048e+09     0.0
2024-10-01 12:00:00  63700.0  63784.0  61100.0  62134.1  242613.990 2024-10-01 17:59:59.999        1.512287e+10         2583155.0                   112641.347                  7.022384e+09     0.0
2024-10-01 18:00:00  62134.1  62422.3  60128.2  60776.8  114948.208 2024-10-01 23:59:59.999        7.031801e+09         1461890.0                    54123.788                  3.312086e+09     0.0
2024-10-02 00:00:00  60776.7  61858.2  60703.3  61466.7   51046.012 2024-10-02 05:59:59.999        3.133969e+09          668558.0                    27191.919                  1.669187e+09     0.0
```

#### Retrieve OHLC data from Bybit Spot for a 1-day interval
```python
from pricehub import get_ohlc

df = get_ohlc(
    broker="bybit_spot",
    symbol="ETHUSDT",
    interval="1d",
    start=1727740800.0, # Unix timestamp for "2024-10-01"
    end=1728086400000, # Unix timestamp for "2024-10-05"
)
print(df)
```

```python
               Open     High      Low    Close        Volume      Turnover
Open time                                                                 
2024-10-01  2602.00  2659.31  2413.15  2447.95  376729.77293  9.623060e+08
2024-10-02  2447.95  2499.82  2351.53  2364.01  242498.88477  5.914189e+08
2024-10-03  2364.01  2403.50  2309.75  2349.91  242598.38255  5.716546e+08
2024-10-04  2349.91  2441.82  2339.15  2414.67  178050.43782  4.254225e+08
2024-10-05  2414.67  2428.69  2389.83  2414.54  106665.69595  2.573030e+08
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
