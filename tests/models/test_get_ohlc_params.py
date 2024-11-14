import pytest
import arrow
from pydantic import ValidationError

from pricehub.models.get_ohlc_params import GetOhlcParams
from pricehub.models.broker import Broker


def test_get_ohlc_params_valid():
    params = GetOhlcParams(
        broker=Broker.BINANCE_SPOT, symbol="BTCUSDT", interval="1h", start="2024-10-01", end="2024-10-02"
    )
    assert params.broker == Broker.BINANCE_SPOT
    assert params.symbol == "BTCUSDT"
    assert params.interval == "1h"
    assert params.start == arrow.get("2024-10-01")
    assert params.end == arrow.get("2024-10-02")


def test_get_ohlc_params_invalid_interval():
    with pytest.raises(ValidationError):
        GetOhlcParams(
            broker=Broker.BINANCE_SPOT,
            symbol="BTCUSDT",
            interval="10m",
            start="2024-10-01",
            end="2024-10-02",
        )


def test_get_ohlc_params_start_after_end():
    with pytest.raises(ValidationError):
        GetOhlcParams(broker=Broker.BINANCE_SPOT, symbol="BTCUSDT", interval="1h", start="2024-10-02", end="2024-10-01")


def test_get_ohlc_params_invalid_date_format():
    with pytest.raises(ValidationError):
        GetOhlcParams(broker=Broker.BINANCE_SPOT, symbol="BTCUSDT", interval="1h", start="date", end="2024-10-02")


def test_get_ohlc_params_invalid_broker():
    with pytest.raises(ValidationError):
        GetOhlcParams(
            broker="binance",
            symbol="BTCUSDT",
            interval="1h",
            start="2024-10-01",
            end="2024-10-02",
        )
