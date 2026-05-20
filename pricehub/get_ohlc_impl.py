"""Top-level entry point for fetching OHLC data from any supported broker."""

import pandas as pd

from pricehub.models import SupportedBroker, Timestamp, GetOhlcParams, Interval


def get_ohlc(
    broker: SupportedBroker, symbol: str, interval: Interval, start: Timestamp, end: Timestamp
) -> pd.DataFrame:
    """Retrieve historical OHLC candles from a supported exchange.

    This is the primary public API. The function normalizes exchange-specific
    response shapes into a pandas DataFrame indexed by ``Open time`` (UTC).
    Pagination across the requested window is handled automatically.

    Example::

        df = get_ohlc(
            broker="binance_spot",
            symbol="BTCUSDT",
            interval="1h",
            start="2024-10-01",
            end="2024-10-02",
        )

    :param broker: Identifier of the broker and market. Must be one of the
        :data:`pricehub.models.types_common.SupportedBroker` literals,
        e.g. ``"binance_spot"``, ``"bybit_linear"``, ``"bitget_futures"``.
    :param symbol: Trading pair symbol in the broker's native format.
        Examples: ``"BTCUSDT"`` (Binance, Bybit, Bitget),
        ``"BTC-USDT"`` (KuCoin, Coinbase), ``"XBTUSD"`` (Kraken).
    :param interval: Candle interval. Must be one of the
        :data:`pricehub.models.types_common.Interval` literals
        (``"1m"``, ``"5m"``, ``"1h"``, ``"1d"``, ``"1w"``, ``"1M"``, ...).
        Not all intervals are supported by every broker.
    :param start: Inclusive start of the time window. Accepts ``int``/``float``
        Unix timestamps (seconds or milliseconds), ISO 8601 strings,
        ``datetime``, ``pandas.Timestamp``, or ``arrow.Arrow``.
    :param end: Exclusive end of the time window. Same accepted formats as
        ``start``. Must be strictly after ``start``.
    :returns: A :class:`pandas.DataFrame` indexed by UTC ``Open time``.
        The exact set of columns depends on the broker; ``Open``, ``High``,
        ``Low``, ``Close``, ``Volume`` are always present.
    :raises ValueError: If the interval is not supported by the chosen broker,
        if the symbol is rejected by the exchange, or if ``start`` is after
        ``end``.
    :raises requests.HTTPError: If the exchange API returns a non-2xx response.
    """
    get_ohlc_params = GetOhlcParams(broker=broker, symbol=symbol, interval=interval, start=start, end=end)
    return get_ohlc_impl(get_ohlc_params)


def get_ohlc_impl(get_ohlc_params: GetOhlcParams) -> pd.DataFrame:
    """Dispatch a validated :class:`GetOhlcParams` to its broker implementation.

    Internal helper used by :func:`get_ohlc`. External callers should prefer
    :func:`get_ohlc`, which validates inputs and accepts loose timestamp types.

    :param get_ohlc_params: Pre-validated request parameters.
    :returns: OHLC data as a :class:`pandas.DataFrame`.
    """
    broker_class = get_ohlc_params.broker.get_broker_class()
    broker_instance = broker_class()
    return broker_instance.get_ohlc(get_ohlc_params)
