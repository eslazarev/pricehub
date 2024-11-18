from pricehub.models.get_ohlc_params import GetOhlcParams
from pricehub.brokers.broker_binance_spot import BrokerBinanceSpot


def test_fetch_data_return(
    mock_binance_get_request_single, get_mock_binance_api_response, get_ohlc_binance_spot_params
):
    broker = BrokerBinanceSpot()
    params = GetOhlcParams(**get_ohlc_binance_spot_params)
    data = broker.fetch_data(params)

    assert data == get_mock_binance_api_response


def test_fetch_data_request_validation(
    mock_binance_get_request_single, get_mock_binance_api_response, get_ohlc_binance_spot_params
):
    broker = BrokerBinanceSpot()
    params = GetOhlcParams(**get_ohlc_binance_spot_params)
    broker.fetch_data(params)

    assert mock_binance_get_request_single.call_count == 1
