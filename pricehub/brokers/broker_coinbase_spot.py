# Updated get_ohlc method in BrokerCoinbase class

import time

import requests

from pricehub.brokers.broker_abc import BrokerABC
import pandas as pd

from pricehub.config import TIMEOUT_SEC


class BrokerCoinbaseSpot(BrokerABC):
    base_url = "https://api.exchange.coinbase.com/products/{symbol}/candles"

    interval_map = {
        "1m": 60,
        "5m": 300,
        "15m": 900,
        "1h": 3600,
        "6h": 21600,
        "1d": 86400,
    }

    def get_ohlc(self, get_ohlc_params: "GetOhlcParams") -> pd.DataFrame:
        self.validate_interval(get_ohlc_params)

        start_time = int(get_ohlc_params.start.timestamp())
        end_time = int(get_ohlc_params.end.timestamp())
        granularity = self.interval_map[get_ohlc_params.interval]

        all_data = []

        # Fetch data in chunks within the 300-row limit
        while start_time < end_time:
            chunk_end_time = min(start_time + (300 * granularity), end_time)

            params = {
                "start": time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime(start_time)),
                "end": time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime(chunk_end_time)),
                "granularity": granularity,
            }

            url = self.base_url.format(symbol=get_ohlc_params.symbol)
            response = requests.get(url, params=params, timeout=TIMEOUT_SEC)
            # response.raise_for_status()
            data = response.json()

            if not data:
                break

            all_data.extend(data)
            start_time = data[0][0] + granularity  # Continue from the next timestamp after the last fetched

            # Check if we reached end
            if chunk_end_time >= end_time:
                break

        if not all_data:
            return pd.DataFrame()

        df = pd.DataFrame(
            all_data,
            columns=["time", "low", "high", "open", "close", "volume"],
        )
        df["time"] = pd.to_datetime(df["time"], unit="s")
        df.set_index("time", inplace=True)
        df.sort_index(inplace=True)

        return df
