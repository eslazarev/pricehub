from unittest.mock import MagicMock

import pytest

from pricehub.brokers import broker_bitget_spot
from pricehub.brokers.broker_bitget_spot import BrokerBitgetSpot
from pricehub.models.get_ohlc_params import GetOhlcParams


@pytest.fixture
def get_ohlc_bitget_spot_params():
    return {
        "broker": "bitget_spot",
        "symbol": "BTCUSDT",
        "interval": "1d",
        "start": "2023-11-10T00:00:00Z",
        "end": "2023-11-15T00:00:00Z",
    }


@pytest.fixture
def get_mock_bitget_spot_response_page1():
    return {
        "code": "00000",
        "msg": "success",
        "data": [
            ["1699574400000", "1.0", "2.0", "0.5", "1.5", "100", "150", "150"],
            ["1699660800000", "1.1", "2.1", "0.6", "1.6", "110", "176", "176"],
        ],
    }


@pytest.fixture
def get_mock_bitget_spot_response_page2():
    return {
        "code": "00000",
        "msg": "success",
        "data": [
            ["1699747200000", "1.2", "2.2", "0.7", "1.7", "120", "204", "204"],
            ["1699833600000", "1.3", "2.3", "0.8", "1.8", "130", "234", "234"],
        ],
    }


@pytest.fixture
def mock_bitget_spot_get_request_paginated(
    monkeypatch, get_mock_bitget_spot_response_page1, get_mock_bitget_spot_response_page2
):
    responses = [
        get_mock_bitget_spot_response_page1,
        get_mock_bitget_spot_response_page2,
        {"code": "00000", "msg": "success", "data": []},
    ]
    calls = []

    def fake_get(url, params=None, timeout=None):
        calls.append({"args": (url,), "kwargs": {"params": params, "timeout": timeout}})
        response = MagicMock()
        response.json.return_value = responses.pop(0)
        response.raise_for_status = MagicMock()
        return response

    monkeypatch.setattr(broker_bitget_spot.requests, "get", fake_get)
    return calls


def test_fetch_data_pagination(
    mock_bitget_spot_get_request_paginated,
    get_ohlc_bitget_spot_params,
    get_mock_bitget_spot_response_page1,
    get_mock_bitget_spot_response_page2,
):
    broker = BrokerBitgetSpot()
    params = GetOhlcParams(**get_ohlc_bitget_spot_params)
    data = broker.fetch_data(params)

    expected = [
        [1699574400000, 1.0, 2.0, 0.5, 1.5, 100.0, 150.0, 150.0],
        [1699660800000, 1.1, 2.1, 0.6, 1.6, 110.0, 176.0, 176.0],
        [1699747200000, 1.2, 2.2, 0.7, 1.7, 120.0, 204.0, 204.0],
        [1699833600000, 1.3, 2.3, 0.8, 1.8, 130.0, 234.0, 234.0],
    ]

    assert data == expected
    assert len(mock_bitget_spot_get_request_paginated) == 3

    first_call, second_call, third_call = mock_bitget_spot_get_request_paginated
    start_ms = int(params.start.timestamp() * 1000)
    end_ms = int(params.end.timestamp() * 1000)

    assert first_call["args"][0] == broker.api_url
    assert first_call["kwargs"]["params"]["startTime"] == start_ms
    assert first_call["kwargs"]["params"]["endTime"] == end_ms
    assert first_call["kwargs"]["params"]["symbol"] == "BTCUSDT"
    assert first_call["kwargs"]["params"]["granularity"] == "1day"

    expected_cursor_2 = int(get_mock_bitget_spot_response_page1["data"][-1][0]) + 1
    expected_cursor_3 = int(get_mock_bitget_spot_response_page2["data"][-1][0]) + 1

    assert second_call["kwargs"]["params"]["startTime"] == expected_cursor_2
    assert third_call["kwargs"]["params"]["startTime"] == expected_cursor_3


def test_api_error_raises(monkeypatch, get_ohlc_bitget_spot_params):
    def fake_get(url, params=None, timeout=None):
        response = MagicMock()
        response.json.return_value = {"code": "40001", "msg": "Invalid symbol", "data": []}
        response.raise_for_status = MagicMock()
        return response

    monkeypatch.setattr(broker_bitget_spot.requests, "get", fake_get)

    broker = BrokerBitgetSpot()
    params = GetOhlcParams(**get_ohlc_bitget_spot_params)
    with pytest.raises(ValueError, match="Bitget API error: Invalid symbol"):
        broker.fetch_data(params)


def test_invalid_interval_raises(get_ohlc_bitget_spot_params):
    broker = BrokerBitgetSpot()
    bad_params = {**get_ohlc_bitget_spot_params, "interval": "2h"}
    params = GetOhlcParams(**bad_params)
    with pytest.raises(ValueError, match="Interval '2h' is not supported"):
        broker.validate_interval(params)


def test_convert_to_dataframe(get_mock_bitget_spot_response_page1):
    broker = BrokerBitgetSpot()
    raw = get_mock_bitget_spot_response_page1["data"]
    aggregated = [
        [
            int(row[0]),
            float(row[1]),
            float(row[2]),
            float(row[3]),
            float(row[4]),
            float(row[5]),
            float(row[6]),
            float(row[7]),
        ]
        for row in raw
    ]
    df = broker.convert_to_dataframe(aggregated)
    assert list(df.columns) == ["Open", "High", "Low", "Close", "Volume", "Quote volume", "USDT volume"]
    assert df.index.name == "Open time"
    assert len(df) == 2
    assert df["Close"].iloc[0] == 1.5
