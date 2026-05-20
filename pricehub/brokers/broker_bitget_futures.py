"""Bitget Futures (USDT-M Perpetual) broker implementation."""

from typing import Dict, List

import pandas as pd
import requests

from pricehub.brokers.broker_abc import BrokerABC
from pricehub.config import TIMEOUT_SEC


class BrokerBitgetFutures(BrokerABC):
    """
    Bitget Futures Broker — USDT-M Perpetual (historical)
    https://www.bitget.com/api-doc/contract/market/Get-Candle-Data
    """

    api_url = "https://api.bitget.com/api/v2/mix/market/history-candles"
    product_type = "USDT-FUTURES"
    columns = ["Open time", "Open", "High", "Low", "Close", "Volume", "Quote volume"]

    interval_map = {
        "1m": "1m",
        "3m": "3m",
        "5m": "5m",
        "15m": "15m",
        "30m": "30m",
        "1h": "1H",
        "4h": "4H",
        "6h": "6H",
        "12h": "12H",
        "1d": "1D",
        "1w": "1W",
        "1M": "1M",
    }

    page_limit = 200

    def fetch_data(self, get_ohlc_params: "GetOhlcParams") -> List[list]:  # type: ignore[name-defined]
        start_ms = int(get_ohlc_params.start.timestamp() * 1000)
        end_ms = int(get_ohlc_params.end.timestamp() * 1000)
        granularity = self.interval_map[get_ohlc_params.interval]

        cursor_ms = start_ms
        aggregated: Dict[int, list] = {}

        while cursor_ms < end_ms:
            params = {
                "symbol": get_ohlc_params.symbol,
                "productType": self.product_type,
                "granularity": granularity,
                "startTime": cursor_ms,
                "endTime": end_ms,
                "limit": self.page_limit,
            }
            resp = requests.get(self.api_url, params=params, timeout=TIMEOUT_SEC)
            resp.raise_for_status()
            payload = resp.json()
            if payload.get("code") != "00000":
                raise ValueError(f"Bitget Futures API error: {payload.get('msg', 'unknown error')}")

            data = payload.get("data", [])
            if not data:
                break

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

            last_ts = int(data[-1][0])
            if last_ts <= cursor_ms:
                break
            cursor_ms = last_ts + 1

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
                "Quote volume": float,
            }
        )
        df.set_index("Open time", inplace=True)
        df.sort_index(inplace=True)
        return df
