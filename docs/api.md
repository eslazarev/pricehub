# API Reference

## `get_ohlc`

```python
def get_ohlc(
    broker: SupportedBroker,
    symbol: str,
    interval: Interval,
    start: Timestamp,
    end: Timestamp,
) -> pandas.DataFrame
```

Retrieves OHLC data for the specified broker, symbol, interval, and date range. Pagination across the requested window is handled automatically.

### Parameters

| Name | Type | Description |
|------|------|-------------|
| `broker` | `str` | Identifier of the broker and market (see [Supported Brokers](#supported-brokers)) |
| `symbol` | `str` | Trading pair symbol in the broker's native format (e.g. `BTCUSDT` for Binance, `BTC-USDT` for KuCoin/Coinbase) |
| `interval` | `str` | Candle interval (`1m`, `5m`, `1h`, `1d`, `1w`, etc.) |
| `start` | `int`, `float`, `str`, `datetime`, `pandas.Timestamp`, or `arrow.Arrow` | Start of the window |
| `end` | same as `start` | End of the window |

### Returns

A `pandas.DataFrame` indexed by `Open time` with columns dependent on the broker. The common subset is:

- `Open`, `High`, `Low`, `Close` — prices
- `Volume` — base asset volume

Broker-specific extras are preserved (for example, Binance returns `Number of trades`, `Quote asset volume`, `Taker buy base asset volume`, `Taker buy quote asset volume`).

### Raises

- `requests.HTTPError` — when the exchange API returns a non-2xx response after retries
- `ValueError` — when the broker name, interval, or symbol is invalid for the chosen broker

## Supported Brokers

| Broker String      | Exchange | Market   |
|--------------------|----------|----------|
| `binance_spot`     | Binance  | Spot     |
| `binance_futures`  | Binance  | Futures (USDT-M) |
| `bybit_spot`       | Bybit    | Spot     |
| `bybit_linear`     | Bybit    | Linear futures |
| `bybit_inverse`    | Bybit    | Inverse futures |
| `coinbase_spot`    | Coinbase | Spot     |
| `okx_spot`         | OKX      | Spot     |
| `okx_futures`      | OKX      | Futures  |
| `kraken_spot`      | Kraken   | Spot     |
| `kucoin_spot`      | KuCoin   | Spot     |
| `kucoin_futures`   | KuCoin   | Futures  |
| `bitget_spot`      | Bitget   | Spot     |
| `bitget_futures`   | Bitget   | Futures (USDT-M Perpetual) |

## Type Aliases

- `SupportedBroker` — string literal type enumerating all broker identifiers above
- `Interval` — string literal type enumerating supported intervals (`1m`, `5m`, `1h`, `1d`, etc.)
- `Timestamp` — union of `int`, `float`, `str`, `datetime.datetime`, `pandas.Timestamp`, `arrow.Arrow`
