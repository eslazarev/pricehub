from unittest.mock import MagicMock

import pytest

from pricehub.brokers import broker_kraken_spot
from pricehub.brokers.broker_kraken_spot import BrokerKrakenSpot
from pricehub.models.get_ohlc_params import GetOhlcParams


@pytest.fixture
def get_ohlc_kraken_spot_params():
    return {
        "broker": "kraken_spot",
        "symbol": "XBTUSD",
        "interval": "1d",
        "start": "2023-11-10T00:00:00Z",
        "end": "2023-11-15T00:00:00Z",
    }


@pytest.fixture
def get_mock_kraken_api_response_page1():
    return {
        "error": [],
        "result": {
            "XBTUSD": [
                [1700000000, "1", "2", "0.5", "1.5", "1.1", "100", 10],
                [1699913600, "1.1", "2.1", "0.6", "1.6", "1.2", "110", 11],
            ],
            "last": "1699913600",
        },
    }


@pytest.fixture
def get_mock_kraken_api_response_page2():
    return {
        "error": [],
        "result": {
            "XBTUSD": [
                [1699827200, "1.2", "2.2", "0.7", "1.7", "1.3", "120", 12],
                [1699740800, "1.3", "2.3", "0.8", "1.8", "1.4", "130", 13],
            ],
            "last": "1699740800",
        },
    }


@pytest.fixture
def mock_kraken_get_request_paginated(
    monkeypatch, get_mock_kraken_api_response_page1, get_mock_kraken_api_response_page2
):
    responses = [
        get_mock_kraken_api_response_page1,
        get_mock_kraken_api_response_page2,
        {"error": [], "result": {"XBTUSD": [], "last": "1699740800"}},
    ]
    calls = []

    def fake_get(url, params=None, timeout=None):
        calls.append({"args": (url,), "kwargs": {"params": params, "timeout": timeout}})
        response = MagicMock()
        response.json.return_value = responses.pop(0)
        response.raise_for_status = MagicMock()
        return response

    monkeypatch.setattr(broker_kraken_spot.requests, "get", fake_get)
    return calls


def test_fetch_data_pagination(
    mock_kraken_get_request_paginated,
    get_ohlc_kraken_spot_params,
    get_mock_kraken_api_response_page1,
    get_mock_kraken_api_response_page2,
):
    broker = BrokerKrakenSpot()
    params = GetOhlcParams(**get_ohlc_kraken_spot_params)
    data = broker.fetch_data(params)

    expected = [
        [1699740800000, 1.3, 2.3, 0.8, 1.8, 1.4, 130.0, 13],
        [1699827200000, 1.2, 2.2, 0.7, 1.7, 1.3, 120.0, 12],
        [1699913600000, 1.1, 2.1, 0.6, 1.6, 1.2, 110.0, 11],
        [1700000000000, 1.0, 2.0, 0.5, 1.5, 1.1, 100.0, 10],
    ]

    assert data == expected
    assert len(mock_kraken_get_request_paginated) == 2

    first_call, second_call = mock_kraken_get_request_paginated
    start_s = int(params.start.timestamp())

    assert first_call["args"][0] == broker.api_url
    assert first_call["kwargs"]["params"]["since"] == start_s

    first_since = int(get_mock_kraken_api_response_page1["result"]["last"])
    assert second_call["kwargs"]["params"]["since"] == first_since
