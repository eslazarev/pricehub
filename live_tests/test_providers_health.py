"""End-to-end health check against live exchange APIs.

Hits every supported broker with a small recent window and asserts that
real data is returned. Not part of the unit test suite — run only by the
``providers-health.yml`` GitHub Actions workflow on a daily schedule.
"""

import datetime

import pytest

from pricehub import get_ohlc

BROKER_SYMBOLS = {
    "binance_spot": "BTCUSDT",
    "binance_futures": "BTCUSDT",
    "bybit_spot": "BTCUSDT",
    "bybit_linear": "BTCUSDT",
    "bybit_inverse": "BTCUSD",
    "coinbase_spot": "BTC-USD",
    "okx_spot": "BTC-USDT",
    "okx_futures": "BTC-USDT-SWAP",
    "kraken_spot": "XBTUSD",
    "kucoin_spot": "BTC-USDT",
    "kucoin_futures": "XBTUSDTM",
    "bitget_spot": "BTCUSDT",
    "bitget_futures": "BTCUSDT",
}


@pytest.mark.parametrize("broker,symbol", sorted(BROKER_SYMBOLS.items()))
def test_broker_returns_recent_data(broker: str, symbol: str) -> None:
    """Verify a broker returns at least one valid daily candle from the last 3 days."""
    now = datetime.datetime.now(datetime.timezone.utc)
    end = now - datetime.timedelta(hours=2)
    start = end - datetime.timedelta(days=3)

    df = get_ohlc(broker, symbol, "1d", start, end)

    assert len(df) > 0, f"{broker} returned empty DataFrame for {symbol}"
    assert df["Close"].iloc[-1] > 0, f"{broker} returned non-positive Close price for {symbol}"
    assert df["Open"].iloc[-1] > 0, f"{broker} returned non-positive Open price for {symbol}"
