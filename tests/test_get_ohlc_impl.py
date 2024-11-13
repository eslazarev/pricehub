import pytest
from unittest.mock import patch
import pandas as pd
from pricehub.get_ohlc_impl import get_ohlc, get_ohlc_impl
from pricehub.models import GetOhlcParams


@pytest.fixture
def ohlc_test_data():
    return {"broker": "binance_spot", "symbol": "BTCUSDT", "interval": "1h", "start": "2024-10-01", "end": "2024-10-02"}


@pytest.fixture
def mock_df():
    return pd.DataFrame(
        {
            "Open time": pd.to_datetime(["2024-10-01 00:00", "2024-10-01 01:00"]),
            "Open": [10000, 10100],
            "High": [10200, 10300],
            "Low": [9900, 10000],
            "Close": [10100, 10200],
            "Volume": [1.5, 2.0],
        }
    )


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
