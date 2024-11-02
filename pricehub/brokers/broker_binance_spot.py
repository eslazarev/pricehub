""" Binance Spot Broker """

from pricehub.brokers.broker_binance import BrokerBinanceABC


class BrokerBinanceSpot(BrokerBinanceABC):
    """Binance Spot Broker"""

    base_url = "https://api.binance.com/api/v3/klines"
