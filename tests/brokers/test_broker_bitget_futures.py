from unittest.mock import MagicMock

import pytest

from pricehub.brokers import broker_bitget_futures
from pricehub.brokers.broker_bitget_futures import BrokerBitgetFutures
from pricehub.models.get_ohlc_params import GetOhlcParams


@pytest.fixture
def get_ohlc_bitget_futures_params():
    return {
        "broker": "bitget_futures",
        "symbol": "BTCUSDT",
        "interval": "1h",
        "start": "2023-11-10T00:00:00Z",
        "end": "2023-11-10T04:00:00Z",
    }


@pytest.fixture
def get_mock_bitget_futures_response_page1():
    return {
        "code": "00000",
        "msg": "success",
        "data": [
            ["1699574400000", "1.0", "2.0", "0.5", "1.5", "100", "150"],
            ["1699578000000", "1.1", "2.1", "0.6", "1.6", "110", "176"],
        ],
    }


@pytest.fixture
def get_mock_bitget_futures_response_page2():
    return {
        "code": "00000",
        "msg": "success",
        "data": [
            ["1699581600000", "1.2", "2.2", "0.7", "1.7", "120", "204"],
            ["1699585200000", "1.3", "2.3", "0.8", "1.8", "130", "234"],
        ],
    }


@pytest.fixture
def mock_bitget_futures_get_request_paginated(
    monkeypatch, get_mock_bitget_futures_response_page1, get_mock_bitget_futures_response_page2
):
    responses = [
        get_mock_bitget_futures_response_page1,
        get_mock_bitget_futures_response_page2,
        {"code": "00000", "msg": "success", "data": []},
    ]
    calls = []

    def fake_get(url, params=None, timeout=None):
        calls.append({"args": (url,), "kwargs": {"params": params, "timeout": timeout}})
        response = MagicMock()
        response.json.return_value = responses.pop(0)
        response.raise_for_status = MagicMock()
        return response

    monkeypatch.setattr(broker_bitget_futures.requests, "get", fake_get)
    return calls


def test_fetch_data_pagination(
    mock_bitget_futures_get_request_paginated,
    get_ohlc_bitget_futures_params,
    get_mock_bitget_futures_response_page1,
):
    broker = BrokerBitgetFutures()
    params = GetOhlcParams(**get_ohlc_bitget_futures_params)
    data = broker.fetch_data(params)

    expected = [
        [1699574400000, 1.0, 2.0, 0.5, 1.5, 100.0, 150.0],
        [1699578000000, 1.1, 2.1, 0.6, 1.6, 110.0, 176.0],
        [1699581600000, 1.2, 2.2, 0.7, 1.7, 120.0, 204.0],
        [1699585200000, 1.3, 2.3, 0.8, 1.8, 130.0, 234.0],
    ]

    assert data == expected
    assert len(mock_bitget_futures_get_request_paginated) == 3

    first_call = mock_bitget_futures_get_request_paginated[0]
    assert first_call["args"][0] == broker.api_url
    assert first_call["kwargs"]["params"]["productType"] == "USDT-FUTURES"
    assert first_call["kwargs"]["params"]["granularity"] == "1H"

    expected_cursor_2 = int(get_mock_bitget_futures_response_page1["data"][-1][0]) + 1
    assert mock_bitget_futures_get_request_paginated[1]["kwargs"]["params"]["startTime"] == expected_cursor_2


def test_api_error_raises(monkeypatch, get_ohlc_bitget_futures_params):
    def fake_get(url, params=None, timeout=None):
        response = MagicMock()
        response.json.return_value = {"code": "40001", "msg": "Invalid contract", "data": []}
        response.raise_for_status = MagicMock()
        return response

    monkeypatch.setattr(broker_bitget_futures.requests, "get", fake_get)

    broker = BrokerBitgetFutures()
    params = GetOhlcParams(**get_ohlc_bitget_futures_params)
    with pytest.raises(ValueError, match="Bitget Futures API error: Invalid contract"):
        broker.fetch_data(params)


def test_convert_to_dataframe(get_mock_bitget_futures_response_page1):
    broker = BrokerBitgetFutures()
    aggregated = [
        [
            int(row[0]),
            float(row[1]),
            float(row[2]),
            float(row[3]),
            float(row[4]),
            float(row[5]),
            float(row[6]),
        ]
        for row in get_mock_bitget_futures_response_page1["data"]
    ]
    df = broker.convert_to_dataframe(aggregated)
    assert list(df.columns) == ["Open", "High", "Low", "Close", "Volume", "Quote volume"]
    assert df.index.name == "Open time"
    assert len(df) == 2
