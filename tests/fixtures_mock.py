from unittest.mock import MagicMock


import pytest
import pandas as pd


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


@pytest.fixture
def mock_binance_spot_api_response():
    return [
        [
            1731196800000,
            "76677.46000000",
            "81500.00000000",
            "76492.00000000",
            "80370.01000000",
            "61830.10043500",
            1731283199999,
            "4905441473.90073684",
            7128598,
            "32751.01217700",
            "2597409399.23496312",
            "0",
        ],
        [
            1731283200000,
            "80370.01000000",
            "89530.54000000",
            "80216.01000000",
            "88647.99000000",
            "82323.66577600",
            1731369599999,
            "6944268709.94272134",
            9348890,
            "42837.29531400",
            "3613896167.37191224",
            "0",
        ],
    ]


@pytest.fixture
def mock_binance_requests_get_with_side_effect(mocker, mock_binance_spot_api_response):
    mock_requests_get = mocker.patch("pricehub.brokers.broker_binance_abc.requests.get")

    first_response = MagicMock()
    first_response.json.return_value = mock_binance_spot_api_response

    second_response = MagicMock()
    second_response.json.return_value = []

    mock_requests_get.side_effect = [first_response, second_response]
    return mock_requests_get


@pytest.fixture
def get_broker_binance_spot_params():
    return {
        "broker": "binance_spot",
        "symbol": "BTCUSDT",
        "interval": "1d",
        "start": "2024.11.10",
        "end": "2024.11.11",
    }
