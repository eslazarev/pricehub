"""Broker Enum class"""

from enum import Enum

from pricehub.brokers.broker_binance_futures import BrokerBinanceFutures
from pricehub.brokers.broker_binance_spot import BrokerBinanceSpot
from pricehub.brokers.broker_bybit_inverse import BrokerBybitInverse
from pricehub.brokers.broker_bybit_linear import BrokerBybitLinear
from pricehub.brokers.broker_bybit_spot import BrokerBybitSpot
from pricehub.brokers.broker_coinbase_spot import BrokerCoinbaseSpot
from pricehub.brokers.broker_okx_futures import BrokerOkxFutures
from pricehub.brokers.broker_okx_spot import BrokerOkxSpot


class Broker(Enum):
    """
    Broker Enum class
    """

    BINANCE_SPOT = "binance_spot"
    BINANCE_FUTURES = "binance_futures"
    BYBIT_SPOT = "bybit_spot"
    BYBIT_LINEAR = "bybit_linear"
    BYBIT_INVERSE = "bybit_inverse"
    COINBASE_SPOT = "coinbase_spot"
    OKX_SPOT = "okx_spot"
    OKX_FUTURES = "okx_futures"

    def get_broker_class(self) -> "BrokerABC":  # type: ignore[name-defined]
        """
        Get the broker class for the broker.
        :return:
        """
        broker_classes = {
            Broker.BINANCE_SPOT: BrokerBinanceSpot,
            Broker.BINANCE_FUTURES: BrokerBinanceFutures,
            Broker.BYBIT_SPOT: BrokerBybitSpot,
            Broker.BYBIT_LINEAR: BrokerBybitLinear,
            Broker.BYBIT_INVERSE: BrokerBybitInverse,
            Broker.COINBASE_SPOT: BrokerCoinbaseSpot,
            Broker.OKX_SPOT: BrokerOkxSpot,
            Broker.OKX_FUTURES: BrokerOkxFutures,
        }
        return broker_classes[self]
