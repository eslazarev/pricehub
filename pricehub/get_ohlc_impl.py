""" Get OHLC data from a broker """
import pandas as pd

from pricehub.models import SupportedBroker, Timestamp, GetOhlcParams, Interval


def get_ohlc(
    broker: SupportedBroker, symbol: str, interval: Interval, start: Timestamp, end: Timestamp
) -> pd.DataFrame:
    """
    Get OHLC data from a broker

    Example:

    df = get_ohlc(broker="binance_spot", symbol="BTCUSDT", interval="1h", start="2024-10-01", end="2024-10-02")

    :param interval: Interval of the OHLC data, for example: 1m, 1h, 1d
    :param broker: Name of the broker
    :param symbol: Symbol of the asset
    :param start: Start time of the OHLC data
    :param end: End time of the OHLC data
    :return: OHLC data in a pandas DataFrame
    """
    get_ohlc_params = GetOhlcParams(broker=broker, symbol=symbol, interval=interval, start=start, end=end)
    return get_ohlc_impl(get_ohlc_params)


def get_ohlc_impl(get_ohlc_params: GetOhlcParams) -> pd.DataFrame:
    """
    Get OHLC data from a broker implementation
    :param get_ohlc_params:
    :return: OHLC data in a pandas DataFrame
    """
    broker_class = get_ohlc_params.broker.get_broker_class()
    broker_instance = broker_class()
    return broker_instance.get_ohlc(get_ohlc_params)

