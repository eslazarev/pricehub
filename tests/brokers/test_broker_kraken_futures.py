from unittest.mock import MagicMock

import pytest

from pricehub.brokers import broker_kraken_futures
from pricehub.brokers.broker_kraken_futures import BrokerKrakenFutures
from pricehub.models.get_ohlc_params import GetOhlcParams


@pytest.fixture
def get_ohlc_kraken_futures_params():
    return {
        "broker": "kraken_futures",
        "symbol": "PF_XBTUSD",
        "interval": "1h",
        "start": "2023-11-10T00:00:00Z",
        "end": "2023-11-10T04:00:00Z",
    }


def _candle(ts_ms, o, h, low, c, v):
    return {"time": ts_ms, "open": str(o), "high": str(h), "low": str(low), "close": str(c), "volume": str(v)}


@pytest.fixture
def get_mock_kraken_futures_response_page1():
    return {
        "candles": [
            _candle(1699574400000, 1.0, 2.0, 0.5, 1.5, 100),
            _candle(1699578000000, 1.1, 2.1, 0.6, 1.6, 110),
        ]
    }


@pytest.fixture
def get_mock_kraken_futures_response_page2():
    return {
        "candles": [
            _candle(1699581600000, 1.2, 2.2, 0.7, 1.7, 120),
            _candle(1699585200000, 1.3, 2.3, 0.8, 1.8, 130),
        ]
    }


@pytest.fixture
def mock_kraken_futures_get_request_paginated(
    monkeypatch, get_mock_kraken_futures_response_page1, get_mock_kraken_futures_response_page2
):
    responses = [
        get_mock_kraken_futures_response_page1,
        get_mock_kraken_futures_response_page2,
        {"candles": []},
    ]
    calls = []

    def fake_get(url, params=None, timeout=None):
        calls.append({"args": (url,), "kwargs": {"params": params, "timeout": timeout}})
        response = MagicMock()
        response.json.return_value = responses.pop(0)
        response.raise_for_status = MagicMock()
        return response

    monkeypatch.setattr(broker_kraken_futures.requests, "get", fake_get)
    return calls


def test_fetch_data_pagination(
    mock_kraken_futures_get_request_paginated,
    get_ohlc_kraken_futures_params,
    get_mock_kraken_futures_response_page1,
):
    broker = BrokerKrakenFutures()
    params = GetOhlcParams(**get_ohlc_kraken_futures_params)
    data = broker.fetch_data(params)

    expected = [
        [1699574400000, 1.0, 2.0, 0.5, 1.5, 100.0],
        [1699578000000, 1.1, 2.1, 0.6, 1.6, 110.0],
        [1699581600000, 1.2, 2.2, 0.7, 1.7, 120.0],
        [1699585200000, 1.3, 2.3, 0.8, 1.8, 130.0],
    ]

    assert data == expected
    assert len(mock_kraken_futures_get_request_paginated) == 3

    first_call = mock_kraken_futures_get_request_paginated[0]
    assert first_call["args"][0] == f"{broker.api_url}/PF_XBTUSD/1h"
    start_s = int(params.start.timestamp())
    assert first_call["kwargs"]["params"]["from"] == start_s

    last_ts_page1 = get_mock_kraken_futures_response_page1["candles"][-1]["time"]
    expected_cursor = last_ts_page1 // 1000 + 1
    assert mock_kraken_futures_get_request_paginated[1]["kwargs"]["params"]["from"] == expected_cursor


def test_invalid_interval_raises(get_ohlc_kraken_futures_params):
    broker = BrokerKrakenFutures()
    bad_params = {**get_ohlc_kraken_futures_params, "interval": "2h"}
    params = GetOhlcParams(**bad_params)
    with pytest.raises(ValueError, match="Interval '2h' is not supported"):
        broker.validate_interval(params)


def test_convert_to_dataframe(get_mock_kraken_futures_response_page1):
    broker = BrokerKrakenFutures()
    aggregated = [
        [
            int(row["time"]),
            float(row["open"]),
            float(row["high"]),
            float(row["low"]),
            float(row["close"]),
            float(row["volume"]),
        ]
        for row in get_mock_kraken_futures_response_page1["candles"]
    ]
    df = broker.convert_to_dataframe(aggregated)
    assert list(df.columns) == ["Open", "High", "Low", "Close", "Volume"]
    assert df.index.name == "Open time"
    assert len(df) == 2
    assert df["Close"].iloc[0] == 1.5
