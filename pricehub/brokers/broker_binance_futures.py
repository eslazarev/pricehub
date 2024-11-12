""" Binance Futures Broker Class """

from pricehub.brokers.broker_binance_abc import BrokerBinanceABC


class BrokerBinanceFutures(BrokerBinanceABC):
    """
    Binance Futures Broker Class
    """

    api_url = "https://fapi.binance.com/fapi/v1/klines"

    interval_map = {
        "1m": "1m",
        "3m": "3m",
        "5m": "5m",
        "15m": "15m",
        "30m": "30m",
        "1h": "1h",
        "2h": "2h",
        "4h": "4h",
        "6h": "6h",
        "12h": "12h",
        "1d": "1d",
        "1w": "1w",
        "1M": "1M",
    }
