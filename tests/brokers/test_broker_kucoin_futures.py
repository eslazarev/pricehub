from unittest.mock import MagicMock

import pytest

from pricehub.brokers import broker_kucoin_futures
from pricehub.brokers.broker_kucoin_futures import BrokerKucoinFutures
from pricehub.models.get_ohlc_params import GetOhlcParams


@pytest.fixture
def get_ohlc_kucoin_futures_params():
    return {
        "broker": "kucoin_futures",
        "symbol": "XBTUSDTM",
        "interval": "1m",
        "start": "2023-11-14T22:13:20Z",
        "end": "2023-11-14T22:17:20Z",
    }


@pytest.fixture
def get_mock_kucoin_futures_response_page1():
    return {
        "code": "200000",
        "data": [
            [1700000000000, 1.0, 2.0, 0.5, 1.5, 10.0, 100.0],
            [1700000060000, 1.1, 2.1, 0.6, 1.6, 11.0, 110.0],
        ],
    }


@pytest.fixture
def get_mock_kucoin_futures_response_page2():
    return {
        "code": "200000",
        "data": [
            [1700000120000, 1.2, 2.2, 0.7, 1.7, 12.0, 120.0],
            [1700000180000, 1.3, 2.3, 0.8, 1.8, 13.0, 130.0],
        ],
    }


@pytest.fixture
def mock_kucoin_futures_get_request_paginated(
    monkeypatch, get_mock_kucoin_futures_response_page1, get_mock_kucoin_futures_response_page2
):
    responses = [
        get_mock_kucoin_futures_response_page1,
        get_mock_kucoin_futures_response_page2,
        {"code": "200000", "data": []},
    ]
    calls = []

    def fake_get(url, params=None, timeout=None):
        calls.append({"args": (url,), "kwargs": {"params": params, "timeout": timeout}})
        response = MagicMock()
        response.json.return_value = responses.pop(0)
        response.raise_for_status = MagicMock()
        return response

    monkeypatch.setattr(broker_kucoin_futures.requests, "get", fake_get)
    return calls


def test_fetch_data_pagination(
    mock_kucoin_futures_get_request_paginated,
    get_ohlc_kucoin_futures_params,
    get_mock_kucoin_futures_response_page1,
):
    broker = BrokerKucoinFutures()
    params = GetOhlcParams(**get_ohlc_kucoin_futures_params)
    data = broker.fetch_data(params)

    expected = [
        [1700000000000, 1.0, 2.0, 0.5, 1.5, 10.0, 100.0],
        [1700000060000, 1.1, 2.1, 0.6, 1.6, 11.0, 110.0],
        [1700000120000, 1.2, 2.2, 0.7, 1.7, 12.0, 120.0],
        [1700000180000, 1.3, 2.3, 0.8, 1.8, 13.0, 130.0],
    ]

    assert data == expected
    assert len(mock_kucoin_futures_get_request_paginated) == 3

    first_call, second_call, _third_call = mock_kucoin_futures_get_request_paginated
    start_ms = int(params.start.timestamp() * 1000)
    end_ms = int(params.end.timestamp() * 1000)
    gran_ms = broker.interval_map[params.interval] * 60 * 1000

    assert first_call["args"][0] == broker.api_url
    assert first_call["kwargs"]["params"]["from"] == start_ms
    assert first_call["kwargs"]["params"]["to"] == end_ms

    last_ts = get_mock_kucoin_futures_response_page1["data"][-1][0]
    assert second_call["kwargs"]["params"]["from"] == last_ts + gran_ms
