""" Bybit Spot broker implementation """
import requests
import pandas as pd
from pricehub.brokers.broker_abc import BrokerABC
from pricehub.config import TIMEOUT_SEC


class BrokerBybitSpot(BrokerABC):
    """
    Bybit Spot broker implementation
    https://bybit-exchange.github.io/docs/v5/market/kline
    """

    base_url = "https://api.bybit.com/v5/market/kline"

    interval_map = {
        "1m": "1",
        "3m": "3",
        "5m": "5",
        "15m": "15",
        "30m": "30",
        "1h": "60",
        "2h": "120",
        "4h": "240",
        "6h": "360",
        "12h": "720",
        "1d": "D",
        "1w": "W",
        "1M": "M",
    }

    def get_ohlc(self, get_ohlc_params: "GetOhlcParams") -> pd.DataFrame:  # type: ignore[name-defined]
        interval = self.interval_map.get(get_ohlc_params.interval)
        if not interval:
            raise ValueError(f"Interval '{get_ohlc_params.interval}' is not supported by Bybit.")

        start_time = int(get_ohlc_params.start.timestamp() * 1000)
        end_time = int(get_ohlc_params.end.timestamp() * 1000)

        params = {
            "category": "spot",
            "symbol": get_ohlc_params.symbol,
            "interval": interval,
            "start": start_time,
            "end": end_time,
            "limit": 200,
        }

        all_data = []

        while True:
            response = requests.get(self.base_url, params=params, timeout=TIMEOUT_SEC)
            data = response.json()

            if data["retCode"] != 0:
                raise ValueError(f"Bybit API error: {data['retMsg']}")

            result = data["result"]
            if not result["list"]:
                break

            batch_data = result["list"][::-1]
            all_data.extend(batch_data)

            if len(result["list"]) < params["limit"]:
                break

            earliest_timestamp = int(batch_data[0][0])
            params["end"] = earliest_timestamp - 1

            if params["end"] < start_time:
                break

        if not all_data:
            return pd.DataFrame()

        all_data = all_data[::-1]

        df = pd.DataFrame(
            all_data,
            columns=["Open time", "Open", "High", "Low", "Close", "Volume", "Turnover"],
        )
        df["Open time"] = pd.to_datetime(df["Open time"].astype(int), unit="ms")
        df = df.astype({"Open": float, "High": float, "Low": float, "Close": float, "Volume": float, "Turnover": float})
        df.set_index("Open time", inplace=True)

        df.sort_index(inplace=True)

        return df
