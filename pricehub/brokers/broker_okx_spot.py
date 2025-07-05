import requests
import pandas as pd
from typing import List

from pricehub.brokers.broker_abc import BrokerABC
from pricehub.config import TIMEOUT_SEC


class BrokerOkxSpot(BrokerABC):
    """
    OKX Spot Broker (historical)
    https://www.okx.com/docs-v5/en/#rest-api-market-data-get-history-candles
    """

    api_url = "https://www.okx.com/api/v5/market/history-candles"
    columns = ["Open time", "Open", "High", "Low", "Close", "Volume"]

    interval_map = {
        "1m": "1m",
        "5m": "5m",
        "15m": "15m",
        "1h": "1H",
        "6h": "6H",
        "1d": "1D",
    }

    maximum_data_points = 1000

    def fetch_data(self, get_ohlc_params: "GetOhlcParams") -> List[list]:  # type: ignore[name-defined]
        start_ms = int(get_ohlc_params.start.timestamp() * 1000)
        end_ms = int(get_ohlc_params.end.timestamp() * 1000)
        granularity = self.interval_map[get_ohlc_params.interval]

        aggregated = []

        while True:
            params = {
                "instId": get_ohlc_params.symbol,
                "bar": granularity,
                "limit": self.maximum_data_points,
                "after": end_ms,
            }
            resp = requests.get(self.api_url, params=params, timeout=TIMEOUT_SEC)
            resp.raise_for_status()
            data = resp.json().get("data", [])
            if not data:
                break

            for row in data:
                ts = int(row[0])

                if ts < start_ms or ts > end_ms:
                    continue

                aggregated.append(
                    [
                        ts,
                        float(row[1]),
                        float(row[2]),
                        float(row[3]),
                        float(row[4]),
                        float(row[5]),
                    ]
                )

            if int(data[-1][0]) <= start_ms:
                break

            end_ms = int(data[0][0]) * 1000 - 1

        return aggregated[::-1]

    def convert_to_dataframe(self, aggregated_data: list) -> pd.DataFrame:
        df = pd.DataFrame(aggregated_data, columns=self.columns)
        df["Open time"] = pd.to_datetime(df["Open time"], unit="ms", utc=True)
        df.set_index("Open time", inplace=True)
        df.sort_index(inplace=True)
        return df
