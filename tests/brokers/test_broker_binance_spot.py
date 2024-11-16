from pricehub.models.get_ohlc_params import GetOhlcParams
from pricehub.brokers.broker_binance_spot import BrokerBinanceSpot

from tests.fixtures_mock import (
    mock_binance_spot_api_response,
    get_broker_binance_spot_params,
    mock_binance_requests_get_with_side_effect,
)


def test_fetch_data(
    mock_binance_requests_get_with_side_effect, mock_binance_spot_api_response, get_broker_binance_spot_params
):
    broker = BrokerBinanceSpot()
    params = GetOhlcParams(**get_broker_binance_spot_params)
    data = broker.fetch_data(params)

    assert data == mock_binance_spot_api_response
