"""KuCoin Spot broker implementation."""

from typing import Dict, List

import pandas as pd
import requests

from pricehub.brokers.broker_abc import BrokerABC
from pricehub.config import TIMEOUT_SEC


class BrokerKucoinSpot(BrokerABC):
    """
    KuCoin Spot Broker (historical)
    https://www.kucoin.com/docs/rest/spot-trading/market-data/get-klines
    """

    api_url = "https://api.kucoin.com/api/v1/market/candles"
    columns = ["Open time", "Open", "High", "Low", "Close", "Volume", "Turnover"]

    interval_map = {
        "1m": "1min",
        "3m": "3min",
        "5m": "5min",
        "15m": "15min",
        "30m": "30min",
        "1h": "1hour",
        "2h": "2hour",
        "4h": "4hour",
        "6h": "6hour",
        "8h": "8hour",
        "12h": "12hour",
        "1d": "1day",
        "1w": "1week",
    }

    def fetch_data(self, get_ohlc_params: "GetOhlcParams") -> List[list]:  # type: ignore[name-defined]
        start_ms = int(get_ohlc_params.start.timestamp() * 1000)
        end_ms = int(get_ohlc_params.end.timestamp() * 1000)
        interval = self.interval_map[get_ohlc_params.interval]

        start_s = start_ms // 1000
        cursor_s = end_ms // 1000
        aggregated: Dict[int, list] = {}

        while True:
            params = {
                "symbol": get_ohlc_params.symbol,
                "type": interval,
                "startAt": start_s,
                "endAt": cursor_s,
            }
            resp = requests.get(self.api_url, params=params, timeout=TIMEOUT_SEC)
            resp.raise_for_status()
            payload = resp.json()
            if payload.get("code") != "200000":
                raise ValueError(f"KuCoin API error: {payload.get('msg', 'unknown error')}")

            data = payload.get("data", [])
            if not data:
                break

            for row in data:
                ts_ms = int(row[0]) * 1000
                if ts_ms < start_ms or ts_ms > end_ms:
                    continue
                aggregated[ts_ms] = [
                    ts_ms,
                    float(row[1]),
                    float(row[3]),
                    float(row[4]),
                    float(row[2]),
                    float(row[5]),
                    float(row[6]),
                ]

            oldest_s = int(data[-1][0])
            if oldest_s <= start_s:
                break
            if oldest_s >= cursor_s:
                break

            cursor_s = oldest_s - 1

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
                "Volume": float,
                "Turnover": float,
            }
        )
        df.set_index("Open time", inplace=True)
        df.sort_index(inplace=True)
        return df
