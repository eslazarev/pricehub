import pytest

from unittest.mock import MagicMock

from pricehub.brokers import broker_okx_spot
from pricehub.brokers.broker_okx_spot import BrokerOkxSpot
from pricehub.models.get_ohlc_params import GetOhlcParams


@pytest.fixture
def get_ohlc_okx_spot_params():
    return {
        "broker": "okx_spot",
        "symbol": "BTC-USDT",
        "interval": "1d",
        "start": "2023-11-10T00:00:00Z",
        "end": "2023-11-15T00:00:00Z",
    }


@pytest.fixture
def get_mock_okx_api_response_page1():
    return {
        "code": "0",
        "data": [
            ["1700000000000", "1", "2", "0.5", "1.5", "100"],
            ["1699913600000", "1.1", "2.1", "0.6", "1.6", "110"],
        ],
    }


@pytest.fixture
def get_mock_okx_api_response_page2():
    return {
        "code": "0",
        "data": [
            ["1699827200000", "1.2", "2.2", "0.7", "1.7", "120"],
            ["1699740800000", "1.3", "2.3", "0.8", "1.8", "130"],
        ],
    }


@pytest.fixture
def mock_okx_get_request_paginated(
    monkeypatch, get_mock_okx_api_response_page1, get_mock_okx_api_response_page2
):
    responses = [
        get_mock_okx_api_response_page1,
        get_mock_okx_api_response_page2,
        {"code": "0", "data": []},
    ]
    calls = []

    def fake_get(url, params=None, timeout=None):
        calls.append({"args": (url,), "kwargs": {"params": params, "timeout": timeout}})
        response = MagicMock()
        response.json.return_value = responses.pop(0)
        response.raise_for_status = MagicMock()
        return response

    monkeypatch.setattr(broker_okx_spot.requests, "get", fake_get)
    return calls


def test_fetch_data_pagination(
    mock_okx_get_request_paginated,
    get_ohlc_okx_spot_params,
    get_mock_okx_api_response_page1,
    get_mock_okx_api_response_page2,
):
    broker = BrokerOkxSpot()
    params = GetOhlcParams(**get_ohlc_okx_spot_params)
    data = broker.fetch_data(params)

    expected = [
        [1699740800000, 1.3, 2.3, 0.8, 1.8, 130.0],
        [1699827200000, 1.2, 2.2, 0.7, 1.7, 120.0],
        [1699913600000, 1.1, 2.1, 0.6, 1.6, 110.0],
        [1700000000000, 1.0, 2.0, 0.5, 1.5, 100.0],
    ]

    assert data == expected
    assert len(mock_okx_get_request_paginated) == 3

    first_call, second_call, third_call = mock_okx_get_request_paginated
    end_ms = int(params.end.timestamp() * 1000)

    assert first_call["args"][0] == broker.api_url
    assert first_call["kwargs"]["params"]["after"] == end_ms

    first_cursor = int(get_mock_okx_api_response_page1["data"][-1][0]) - 1
    second_cursor = int(get_mock_okx_api_response_page2["data"][-1][0]) - 1

    assert second_call["kwargs"]["params"]["after"] == first_cursor
    assert third_call["kwargs"]["params"]["after"] == second_cursor
