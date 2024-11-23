import pytest

from pricehub.brokers.broker_binance_futures import BrokerBinanceFutures
from pricehub.models.get_ohlc_params import GetOhlcParams
from pricehub.brokers.broker_binance_spot import BrokerBinanceSpot


@pytest.mark.parametrize(
    "broker_class",
    [
        BrokerBinanceSpot,
        BrokerBinanceFutures,
    ],
)
def test_fetch_data_return(
    broker_class, mock_binance_get_request_single, get_mock_binance_api_response, get_ohlc_binance_spot_params
):
    broker = broker_class()
    params = GetOhlcParams(**get_ohlc_binance_spot_params)
    data = broker.fetch_data(params)

    assert data == get_mock_binance_api_response


@pytest.mark.parametrize(
    "broker_class, api_url",
    [
        (BrokerBinanceSpot, "https://api.binance.com/api/v3/klines"),
        (BrokerBinanceFutures, "https://fapi.binance.com/fapi/v1/klines"),
    ],
)
def test_fetch_data_request_validation(
    broker_class, api_url, mock_binance_get_request_single, get_mock_binance_api_response, get_ohlc_binance_spot_params
):
    params = GetOhlcParams(**get_ohlc_binance_spot_params)
    broker = broker_class()
    broker.fetch_data(params)

    assert mock_binance_get_request_single.call_count == 1
    assert mock_binance_get_request_single.call_args[0][0] == (
        f"{api_url}?symbol={params.symbol}&interval={params.interval}"
        f"&startTime={int(params.start.timestamp() * 1000)}&endTime={int(params.end.timestamp() * 1000)}"
    )


@pytest.mark.parametrize(
    "broker_class",
    [
        BrokerBinanceSpot,
        BrokerBinanceFutures,
    ],
)
def test_convert_to_dataframe(broker_class, get_mock_binance_response_df, get_mock_binance_api_response):
    broker = broker_class()
    df = broker.convert_to_dataframe(get_mock_binance_api_response)

    assert df.equals(get_mock_binance_response_df)
