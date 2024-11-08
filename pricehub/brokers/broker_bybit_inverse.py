""" Bybit Spot broker implementation """
from pricehub.brokers.broker_bybit_abc import BrokerBybitABC


class BrokerBybitInverse(BrokerBybitABC):
    """
    Bybit Inverse broker implementation
    https://bybit-exchange.github.io/docs/v5/market/kline
    """

    category = "inverse"
