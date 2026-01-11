"""KuCoin Futures broker implementation."""

from typing import Dict, List

import pandas as pd
import requests

from pricehub.brokers.broker_abc import BrokerABC
from pricehub.config import TIMEOUT_SEC


class BrokerKucoinFutures(BrokerABC):
    """
    KuCoin Futures Broker (historical)
    https://www.kucoin.com/docs/rest/futures-trading/market-data/get-kline-data
    """

    api_url = "https://api-futures.kucoin.com/api/v1/kline/query"
    columns = ["Open time", "Open", "High", "Low", "Close", "Volume", "Turnover"]

    interval_map = {
        "1m": 1,
        "3m": 3,
        "5m": 5,
        "15m": 15,
        "30m": 30,
        "1h": 60,
        "2h": 120,
        "4h": 240,
        "6h": 360,
        "12h": 720,
        "1d": 1440,
        "1w": 10080,
        "1M": 43200,
    }

    def fetch_data(self, get_ohlc_params: "GetOhlcParams") -> List[list]:  # type: ignore[name-defined]
        start_ms = int(get_ohlc_params.start.timestamp() * 1000)
        end_ms = int(get_ohlc_params.end.timestamp() * 1000)
        granularity = self.interval_map[get_ohlc_params.interval]
        step_ms = granularity * 60 * 1000

        cursor_ms = start_ms
        aggregated: Dict[int, list] = {}

        while True:
            params = {
                "symbol": get_ohlc_params.symbol,
                "granularity": granularity,
                "from": cursor_ms,
                "to": end_ms,
            }
            resp = requests.get(self.api_url, params=params, timeout=TIMEOUT_SEC)
            resp.raise_for_status()
            payload = resp.json()
            if payload.get("code") != "200000":
                raise ValueError(f"KuCoin Futures API error: {payload.get('msg', 'unknown error')}")

            data = payload.get("data", [])
            if not data:
                break

            first_ts = int(data[0][0])
            last_ts = int(data[-1][0])
            ascending = first_ts <= last_ts

            for row in data:
                ts_ms = int(row[0])
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
                ]

            if ascending:
                if last_ts >= end_ms or last_ts <= cursor_ms:
                    break
                cursor_ms = last_ts + step_ms
            else:
                if last_ts <= start_ms or last_ts >= cursor_ms:
                    break
                cursor_ms = last_ts - step_ms

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
