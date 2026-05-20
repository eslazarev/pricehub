# For Researchers

PriceHub was designed not only for traders but also for quantitative-finance researchers who need a reproducible, citable, and venue-agnostic data layer.

## Why a Unified Layer Matters for Research

Cryptocurrency markets are fragmented across dozens of venues. Each exchange exposes its own API conventions — endpoints, rate limits, timestamp units, symbol notation, pagination, schema of returned fields. A typical research workflow that compares price discovery or liquidity across venues spends 50–80% of its setup time reconciling these differences before any analysis can begin.

PriceHub absorbs that friction. A single function signature returns a normalized pandas DataFrame, so cross-venue studies become a `for` loop over broker identifiers rather than a separate integration project per exchange.

## Research Use Cases

### Cross-Exchange Price Discovery

```python
import pandas as pd
from pricehub import get_ohlc

venues = ["binance_spot", "bybit_spot", "coinbase_spot", "okx_spot", "kraken_spot"]
closes = pd.concat(
    {v: get_ohlc(v, "BTCUSDT", "1h", "2024-01-01", "2024-12-31")["Close"] for v in venues},
    axis=1,
)
spread = closes.max(axis=1) - closes.min(axis=1)
```

The resulting series quantifies cross-venue spread, useful in studies of market efficiency and arbitrage decay.

### Backtesting Strategy Portability

Strategies developed against a single exchange often fail to replicate when ported to another venue due to subtle data differences. PriceHub lets researchers run an identical backtest pipeline across venues and report robustness as a multi-venue distribution rather than a single point estimate.

### Spot–Futures Basis Studies

```python
spot = get_ohlc("binance_spot", "BTCUSDT", "1h", "2024-01-01", "2024-12-31")
fut = get_ohlc("binance_futures", "BTCUSDT", "1h", "2024-01-01", "2024-12-31")
basis = (fut["Close"] - spot["Close"]) / spot["Close"]
```

Basis behavior across regimes is a common research target; PriceHub aligns the indices so the subtraction is well-defined.

### Market Microstructure Around Macroeconomic Releases

Tick-coarse OHLC at 1-minute intervals around FOMC or CPI release timestamps lets researchers measure realized volatility, jump frequencies, and order-flow imbalance proxies across venues.

## Reproducibility Notes

- **Determinism**: `get_ohlc` returns the same DataFrame given the same arguments, provided the exchange has not amended its historical data (rare but documented for some venues).
- **Date alignment**: All timestamps are returned in UTC with explicit `Open time` indexing, eliminating timezone ambiguity.
- **Version pinning**: For published research, pin `pricehub` to a specific version (`pip install pricehub==X.Y.Z`) and cite that version (see [Citation](citation.md)).
- **Data provenance**: PriceHub returns the raw API response with minimal transformation; field names and units come directly from the exchange documentation.

## Citing PriceHub

If you use PriceHub in academic work, please cite the specific version you used. See the [Citation](citation.md) page for the BibTeX entry and DOI.

## Contributing Research Examples

If you have a published study that used PriceHub, please open an issue or a pull request adding it to this page. Real-world citations help us position the package in the broader quantitative-finance ecosystem.
