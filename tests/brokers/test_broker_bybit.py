import pytest

from pricehub.brokers.broker_bybit_inverse import BrokerBybitInverse
from pricehub.brokers.broker_bybit_linear import BrokerBybitLinear
from pricehub.brokers.broker_bybit_spot import BrokerBybitSpot
from pricehub.models.get_ohlc_params import GetOhlcParams


@pytest.mark.parametrize(
    "broker_class",
    [BrokerBybitSpot, BrokerBybitLinear, BrokerBybitInverse],
)
def test_fetch_data_return(
    broker_class, get_mock_bybit_get_request_single, get_mock_bybit_api_response, get_ohlc_bybit_spot_params
):
    broker = broker_class()
    params = GetOhlcParams(**get_ohlc_bybit_spot_params)
    data = broker.fetch_data(params)

    assert data == get_mock_bybit_api_response["result"]["list"][::-1]
