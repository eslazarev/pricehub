from unittest.mock import patch
from pricehub.get_ohlc_impl import get_ohlc, get_ohlc_impl
from pricehub.models import GetOhlcParams
from tests.fixtures_mock import ohlc_test_data, mock_df


@patch("pricehub.get_ohlc_impl.get_ohlc_impl")
def test_get_ohlc(mock_get_ohlc_impl, ohlc_test_data, mock_df):
    mock_get_ohlc_impl.return_value = mock_df

    result = get_ohlc(**ohlc_test_data)

    assert result.equals(mock_df)
    mock_get_ohlc_impl.assert_called_once_with(GetOhlcParams(**ohlc_test_data))


def test_get_ohlc_impl(ohlc_test_data, mock_df):
    get_ohlc_params = GetOhlcParams(**ohlc_test_data)
    with patch.object(get_ohlc_params.broker.get_broker_class(), "get_ohlc") as mock_get_ohlc:
        mock_get_ohlc.return_value = mock_df

        result = get_ohlc_impl(get_ohlc_params)

        assert result.equals(mock_df)
        mock_get_ohlc.assert_called_once_with(get_ohlc_params)
