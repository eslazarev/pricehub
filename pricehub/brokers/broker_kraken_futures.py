"""Kraken Futures broker implementation."""

from typing import Dict, List

import pandas as pd
import requests

from pricehub.brokers.broker_abc import BrokerABC
from pricehub.config import TIMEOUT_SEC


class BrokerKrakenFutures(BrokerABC):
    """
    Kraken Futures Broker — perpetual and dated contracts (historical)
    https://docs.kraken.com/api/docs/futures-api/charts/get-ohlc

    Symbols use Kraken Futures notation, e.g. ``PF_XBTUSD`` (multi-collateral
    perpetual) or ``PI_XBTUSD`` (inverse perpetual).
    """

    api_url = "https://futures.kraken.com/api/charts/v1/trade"
    columns = ["Open time", "Open", "High", "Low", "Close", "Volume"]

    interval_map = {
        "1m": "1m",
        "5m": "5m",
        "15m": "15m",
        "30m": "30m",
        "1h": "1h",
        "4h": "4h",
        "12h": "12h",
        "1d": "1d",
        "1w": "1w",
    }

    def fetch_data(self, get_ohlc_params: "GetOhlcParams") -> List[list]:  # type: ignore[name-defined]
        start_ms = int(get_ohlc_params.start.timestamp() * 1000)
        end_ms = int(get_ohlc_params.end.timestamp() * 1000)
        resolution = self.interval_map[get_ohlc_params.interval]

        cursor_s = start_ms // 1000
        end_s = end_ms // 1000
        aggregated: Dict[int, list] = {}

        while cursor_s < end_s:
            url = f"{self.api_url}/{get_ohlc_params.symbol}/{resolution}"
            params = {"from": cursor_s, "to": end_s}
            resp = requests.get(url, params=params, timeout=TIMEOUT_SEC)
            resp.raise_for_status()
            payload = resp.json()

            candles = payload.get("candles")
            if not candles:
                break

            for row in candles:
                ts_ms = int(row["time"])
                if ts_ms < start_ms or ts_ms > end_ms:
                    continue
                aggregated[ts_ms] = [
                    ts_ms,
                    float(row["open"]),
                    float(row["high"]),
                    float(row["low"]),
                    float(row["close"]),
                    float(row["volume"]),
                ]

            last_s = int(candles[-1]["time"]) // 1000
            if last_s <= cursor_s:
                break
            cursor_s = last_s + 1

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
            }
        )
        df.set_index("Open time", inplace=True)
        df.sort_index(inplace=True)
        return df
