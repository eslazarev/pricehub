from unittest.mock import patch
from pricehub.get_ohlc_impl import get_ohlc, get_ohlc_impl
from pricehub.models import GetOhlcParams


@patch("pricehub.get_ohlc_impl.get_ohlc_impl")
def test_get_ohlc(mock_get_ohlc_impl, get_ohlc_binance_spot_params, get_mock_binance_response_df):
    mock_get_ohlc_impl.return_value = get_mock_binance_response_df

    result = get_ohlc(**get_ohlc_binance_spot_params)

    assert result.equals(get_mock_binance_response_df)
    mock_get_ohlc_impl.assert_called_once_with(GetOhlcParams(**get_ohlc_binance_spot_params))


def test_get_ohlc_impl(get_ohlc_binance_spot_params, get_mock_binance_response_df):
    get_ohlc_params = GetOhlcParams(**get_ohlc_binance_spot_params)
    with patch.object(get_ohlc_params.broker.get_broker_class(), "get_ohlc") as mock_get_ohlc:
        mock_get_ohlc.return_value = get_mock_binance_response_df

        result = get_ohlc_impl(get_ohlc_params)

        assert result.equals(get_mock_binance_response_df)
        mock_get_ohlc.assert_called_once_with(get_ohlc_params)
