"""Kraken Spot broker implementation."""

from typing import Dict, List

import pandas as pd
import requests

from pricehub.brokers.broker_abc import BrokerABC
from pricehub.config import TIMEOUT_SEC


class BrokerKrakenSpot(BrokerABC):
    """
    Kraken Spot Broker (historical)
    https://docs.kraken.com/rest/#tag/Market-Data/operation/getOHLCData
    """

    api_url = "https://api.kraken.com/0/public/OHLC"
    columns = ["Open time", "Open", "High", "Low", "Close", "VWAP", "Volume", "Count"]

    interval_map = {
        "1m": 1,
        "5m": 5,
        "15m": 15,
        "30m": 30,
        "1h": 60,
        "4h": 240,
        "1d": 1440,
        "1w": 10080,
        "1M": 21600,
    }

    def fetch_data(self, get_ohlc_params: "GetOhlcParams") -> List[list]:  # type: ignore[name-defined]
        start_ms = int(get_ohlc_params.start.timestamp() * 1000)
        end_ms = int(get_ohlc_params.end.timestamp() * 1000)
        interval = self.interval_map[get_ohlc_params.interval]

        since = start_ms // 1000
        aggregated: Dict[int, list] = {}

        while True:
            params = {"pair": get_ohlc_params.symbol, "interval": interval, "since": since}
            resp = requests.get(self.api_url, params=params, timeout=TIMEOUT_SEC)
            resp.raise_for_status()
            payload = resp.json()
            if payload.get("error"):
                raise ValueError(f"Kraken API error: {payload['error']}")

            result = payload.get("result", {})
            data_key = next((key for key in result.keys() if key != "last"), None)
            if not data_key:
                break

            data = result.get(data_key, [])
            if not data:
                break

            for row in data:
                ts_ms = int(row[0]) * 1000
                if ts_ms < start_ms or ts_ms > end_ms:
                    continue
                aggregated[ts_ms] = [
                    ts_ms,
                    float(row[1]),
                    float(row[2]),
                    float(row[3]),
                    float(row[4]),
                    float(row[5]),
                    float(row[6]),
                    int(row[7]),
                ]

            last = int(result.get("last", since))
            if last <= since or last * 1000 > end_ms:
                break

            since = last

        return [aggregated[key] for key in sorted(aggregated)]

    def convert_to_dataframe(self, aggregated_data: list) -> pd.DataFrame:
        df = pd.DataFrame(aggregated_data, columns=self.columns)
        df["Open time"] = pd.to_datetime(df["Open time"], unit="ms", utc=True)
        df = df.astype(
            {
                "Open": float,
                "High": float,
                "Low": float,
                "Close": float,
                "VWAP": float,
                "Volume": float,
                "Count": int,
            }
        )
        df.set_index("Open time", inplace=True)
        df.sort_index(inplace=True)
        return df
