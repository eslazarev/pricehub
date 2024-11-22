import pytest
import arrow
from pydantic import ValidationError

from pricehub.models.get_ohlc_params import GetOhlcParams
from pricehub.models.broker import Broker


def test_get_ohlc_params_valid(get_ohlc_binance_spot_params):
    params = GetOhlcParams(**get_ohlc_binance_spot_params)
    assert params.broker == Broker.BINANCE_SPOT
    assert params.symbol == get_ohlc_binance_spot_params["symbol"]
    assert params.interval == get_ohlc_binance_spot_params["interval"]
    assert params.start == arrow.get(get_ohlc_binance_spot_params["start"])
    assert params.end == arrow.get(get_ohlc_binance_spot_params["end"])


def test_get_ohlc_params_invalid_interval(get_ohlc_binance_spot_params):
    get_ohlc_binance_spot_params["interval"] = "10m"
    with pytest.raises(ValidationError):
        GetOhlcParams(**get_ohlc_binance_spot_params)


def test_get_ohlc_params_start_after_end(get_ohlc_binance_spot_params):
    get_ohlc_binance_spot_params["start"] = "2024-10-02"
    get_ohlc_binance_spot_params["end"] = "2024-10-01"
    with pytest.raises(ValidationError):
        GetOhlcParams(**get_ohlc_binance_spot_params)


def test_get_ohlc_params_invalid_date_format(get_ohlc_binance_spot_params):
    get_ohlc_binance_spot_params["start"] = "date"
    with pytest.raises(ValidationError):
        GetOhlcParams(**get_ohlc_binance_spot_params)


def test_get_ohlc_params_invalid_broker(get_ohlc_binance_spot_params):
    get_ohlc_binance_spot_params["broker"] = "invalid"
    with pytest.raises(ValidationError):
        GetOhlcParams(**get_ohlc_binance_spot_params)
