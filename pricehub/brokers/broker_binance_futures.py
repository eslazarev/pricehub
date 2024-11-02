""" Binance Futures Broker Class """

from pricehub.brokers.broker_binance import BrokerBinanceABC


class BrokerBinanceFutures(BrokerBinanceABC):
    """
    Binance Futures Broker Class
    """

    base_url = "https://fapi.binance.com/fapi/v1/klines"
