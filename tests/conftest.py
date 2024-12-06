from unittest.mock import MagicMock


import pytest
import pandas as pd


@pytest.fixture
def get_mock_binance_api_response():
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
            "1",
        ],
    ]


@pytest.fixture
def get_mock_binance_response_df(get_mock_binance_api_response):
    df = pd.DataFrame(
        data=get_mock_binance_api_response,
        columns=[
            "Open time",
            "Open",
            "High",
            "Low",
            "Close",
            "Volume",
            "Close time",
            "Quote asset volume",
            "Number of trades",
            "Taker buy base asset volume",
            "Taker buy quote asset volume",
            "Ignore",
        ],
    )
    df = df.astype(float)
    df["Open time"] = pd.to_datetime(df["Open time"], unit="ms")
    df["Close time"] = pd.to_datetime(df["Close time"], unit="ms")
    df.set_index("Open time", inplace=True)
    return df


@pytest.fixture
def mock_binance_get_request_single(mocker, get_mock_binance_api_response):
    mock_requests_get = mocker.patch("pricehub.brokers.broker_binance_abc.requests.get")
    mock_response = MagicMock()
    mock_response.json.return_value = get_mock_binance_api_response
    mock_requests_get.return_value = mock_response

    return mock_requests_get


@pytest.fixture
def mock_binance_get_request_paginated(mocker, get_mock_binance_api_response):
    mock_requests_get = mocker.patch("pricehub.brokers.broker_binance_abc.requests.get")

    first_response = MagicMock()
    first_response.json.return_value = [get_mock_binance_api_response[0]]

    second_response = MagicMock()
    second_response.json.return_value = [get_mock_binance_api_response[1]]

    mock_requests_get.side_effect = [first_response, second_response]
    return mock_requests_get


@pytest.fixture
def mock_binance_get_request_paginated_no_data(mocker, get_mock_binance_api_response):
    mock_requests_get = mocker.patch("pricehub.brokers.broker_binance_abc.requests.get")

    first_response = MagicMock()
    first_response.json.return_value = [get_mock_binance_api_response[0]]

    second_response = MagicMock()
    second_response.json.return_value = []

    mock_requests_get.side_effect = [first_response, second_response]
    return mock_requests_get


@pytest.fixture
def get_ohlc_binance_spot_params():
    return {
        "broker": "binance_spot",
        "symbol": "BTCUSDT",
        "interval": "1d",
        "start": "2024.11.10",
        "end": "2024.11.11",
    }


@pytest.fixture
def get_mock_bybit_api_response():
    return {
        "retCode": 0,
        "retMsg": "OK",
        "result": {
            "category": "spot",
            "symbol": "BTCUSDT",
            "list": [
                ["1731283200000", "80355.85", "89666", "80210.39", "88653.57", "36428.853454", "3051924574.30417488"],
                ["1731196800000", "76670.84", "81518", "76488.71", "80355.85", "28648.21327", "2266259905.05002479"],
            ],
        },
        "retExtInfo": {},
        "time": 1732370687228,
    }


@pytest.fixture
def get_ohlc_bybit_spot_params():
    return {
        "broker": "bybit_spot",
        "symbol": "BTCUSDT",
        "interval": "1d",
        "start": "2024.11.10",
        "end": "2024.11.11",
    }


@pytest.fixture
def get_mock_bybit_get_request_single(mocker, get_mock_bybit_api_response):
    mock_requests_get = mocker.patch("pricehub.brokers.broker_bybit_abc.requests.get")
    mock_response = MagicMock()
    mock_response.json.return_value = get_mock_bybit_api_response
    mock_requests_get.return_value = mock_response

    return mock_requests_get
