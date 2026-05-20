# PriceHub

**Unified Python Package for Collecting OHLC Prices from Cryptocurrency Exchange APIs**

PriceHub provides a single interface to fetch historical OHLC (Open, High, Low, Close) market data from major cryptocurrency exchanges, normalizing exchange-specific quirks into clean pandas DataFrames.

[![PyPI](https://img.shields.io/pypi/v/pricehub.svg)](https://pypi.org/project/pricehub/)
[![License](https://img.shields.io/badge/license-MIT-blue)](https://github.com/eslazarev/pricehub/blob/main/LICENSE)
[![Python Versions](https://img.shields.io/badge/python-3.8%20%7C%203.9%20%7C%203.10%20%7C%203.11%20%7C%203.12%20%7C%203.13-blue)](https://pypi.org/project/pricehub/)

## Why PriceHub?

Effective trading research begins with thorough data analysis, visualization, and backtesting. Each cryptocurrency exchange exposes its own API conventions — timestamp formats, interval naming, pagination strategies, response schemas. PriceHub abstracts these differences into a single function call.

```python
from pricehub import get_ohlc

df = get_ohlc("binance_spot", "BTCUSDT", "1d", "2024-10-01", "2024-10-05")
```

The same call signature works across all supported brokers — switch venues by changing one string.

## Supported Brokers

| Exchange | Spot | Futures |
|----------|:----:|:-------:|
| Binance  | ✅   | ✅      |
| Bybit    | ✅   | ✅ (Linear + Inverse) |
| Coinbase | ✅   | —       |
| OKX      | ✅   | ✅      |
| Kraken   | ✅   | —       |
| KuCoin   | ✅   | ✅      |

## Key Features

- **Unified interface** — one function signature across all brokers and markets
- **Unified intervals** — same interval format (`1m`, `1h`, `1d`, `1w`) across all venues
- **Timestamp flexibility** — accepts `int`, `float`, `str`, Arrow, pandas, and datetime
- **No credentials required** — public market data fetched without API keys
- **Extended date ranges** — automatic pagination across arbitrarily long windows
- **All API fields preserved** — number of trades, taker buy volumes, quote volumes when available
- **Custom intervals** — resample to any frequency pandas understands

## Quick Links

- [Installation](installation.md)
- [Usage Examples](usage.md)
- [API Reference](api.md)
- [For Researchers](for-researchers.md)
- [Citation](citation.md)
- [GitHub Repository](https://github.com/eslazarev/pricehub)
- [PyPI Package](https://pypi.org/project/pricehub/)
