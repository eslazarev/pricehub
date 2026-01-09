"""OKX Futures broker implementation."""

from pricehub.brokers.broker_okx_spot import BrokerOkxSpot


class BrokerOkxFutures(BrokerOkxSpot):
    """
    OKX Futures Broker (historical)
    https://www.okx.com/docs-v5/en/#rest-api-market-data-get-history-candles
    """
