import requests
import pandas as pd
from pricehub.brokers.broker_abc import BrokerABC
import ssl

ssl._create_default_https_context = ssl._create_unverified_context


class BrokerBybitSpot(BrokerABC):
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

        start_time = int(get_ohlc_params.start.timestamp())
        end_time = int(get_ohlc_params.end.timestamp())

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
            response = requests.get(self.base_url, params=params, timeout=10, verify=False)
            data = response.json()

            if data["retCode"] != 0:
                raise Exception(f"Bybit API error: {data['retMsg']}")

            result = data["result"]
            if not result["list"]:
                break

            all_data.extend(result["list"])

            if len(result["list"]) < params["limit"]:
                break

            last_timestamp = int(result["list"][-1][0])
            params["start"] = last_timestamp + 1

        if not all_data:
            return pd.DataFrame()

        df = pd.DataFrame(
            all_data,
            columns=["Open time", "Open", "High", "Low", "Close", "Volume", "Turnover"],
        )
        df["Open time"] = pd.to_datetime(df["Open time"], unit="s")
        df = df.astype({"Open": float, "High": float, "Low": float, "Close": float, "Volume": float, "Turnover": float})
        df.set_index("Open time", inplace=True)

        return df
