from unittest.mock import MagicMock

import pytest

from pricehub.brokers import broker_kucoin_spot
from pricehub.brokers.broker_kucoin_spot import BrokerKucoinSpot
from pricehub.models.get_ohlc_params import GetOhlcParams


@pytest.fixture
def get_ohlc_kucoin_spot_params():
    return {
        "broker": "kucoin_spot",
        "symbol": "BTC-USDT",
        "interval": "1d",
        "start": "2023-11-10T00:00:00Z",
        "end": "2023-11-15T00:00:00Z",
    }


@pytest.fixture
def get_mock_kucoin_spot_response_page1():
    return {
        "code": "200000",
        "data": [
            ["1700000000", "1", "1.5", "2", "0.5", "100", "1000"],
            ["1699913600", "1.1", "1.6", "2.1", "0.6", "110", "1100"],
        ],
    }


@pytest.fixture
def get_mock_kucoin_spot_response_page2():
    return {
        "code": "200000",
        "data": [
            ["1699827200", "1.2", "1.7", "2.2", "0.7", "120", "1200"],
            ["1699740800", "1.3", "1.8", "2.3", "0.8", "130", "1300"],
        ],
    }


@pytest.fixture
def mock_kucoin_spot_get_request_paginated(
    monkeypatch, get_mock_kucoin_spot_response_page1, get_mock_kucoin_spot_response_page2
):
    responses = [
        get_mock_kucoin_spot_response_page1,
        get_mock_kucoin_spot_response_page2,
        {"code": "200000", "data": []},
    ]
    calls = []

    def fake_get(url, params=None, timeout=None):
        calls.append({"args": (url,), "kwargs": {"params": params, "timeout": timeout}})
        response = MagicMock()
        response.json.return_value = responses.pop(0)
        response.raise_for_status = MagicMock()
        return response

    monkeypatch.setattr(broker_kucoin_spot.requests, "get", fake_get)
    return calls


def test_fetch_data_pagination(
    mock_kucoin_spot_get_request_paginated,
    get_ohlc_kucoin_spot_params,
    get_mock_kucoin_spot_response_page1,
    get_mock_kucoin_spot_response_page2,
):
    broker = BrokerKucoinSpot()
    params = GetOhlcParams(**get_ohlc_kucoin_spot_params)
    data = broker.fetch_data(params)

    expected = [
        [1699740800000, 1.3, 2.3, 0.8, 1.8, 130.0, 1300.0],
        [1699827200000, 1.2, 2.2, 0.7, 1.7, 120.0, 1200.0],
        [1699913600000, 1.1, 2.1, 0.6, 1.6, 110.0, 1100.0],
        [1700000000000, 1.0, 2.0, 0.5, 1.5, 100.0, 1000.0],
    ]

    assert data == expected
    assert len(mock_kucoin_spot_get_request_paginated) == 3

    first_call, second_call, third_call = mock_kucoin_spot_get_request_paginated
    start_s = int(params.start.timestamp())
    end_s = int(params.end.timestamp())

    assert first_call["args"][0] == broker.api_url
    assert first_call["kwargs"]["params"]["startAt"] == start_s
    assert first_call["kwargs"]["params"]["endAt"] == end_s

    first_cursor = int(get_mock_kucoin_spot_response_page1["data"][-1][0]) - 1
    second_cursor = int(get_mock_kucoin_spot_response_page2["data"][-1][0]) - 1

    assert second_call["kwargs"]["params"]["endAt"] == first_cursor
    assert third_call["kwargs"]["params"]["endAt"] == second_cursor
