""" This module contains the implementation of the BrokerCoinbaseSpot class. """

import time

import requests
import pandas as pd

from pricehub.brokers.broker_abc import BrokerABC

from pricehub.config import TIMEOUT_SEC


class BrokerCoinbaseSpot(BrokerABC):
    """
    Coinbase Spot Broker
    https://docs.cdp.coinbase.com/exchange/reference/exchangerestapi_getproductcandles

    """

    api_url = "https://api.exchange.coinbase.com/products/{symbol}/candles"
    columns = ["Open time", "Low", "High", "Open", "Close", "Volume"]

    interval_map = {
        "1m": 60,
        "5m": 300,
        "15m": 900,
        "1h": 3600,
        "6h": 21600,
        "1d": 86400,
    }
    maximum_data_points = 300

    def fetch_data(self, get_ohlc_params: "GetOhlcParams") -> list:  # type: ignore[name-defined]
        start_time = int(get_ohlc_params.start.timestamp())
        end_time = int(get_ohlc_params.end.timestamp())
        granularity = self.interval_map[get_ohlc_params.interval]

        aggregated_data = []

        while start_time < end_time:
            chunk_end_time = min(start_time + (self.maximum_data_points * granularity), end_time)

            params = {
                "start": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(start_time)),
                "end": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(chunk_end_time)),
                "granularity": granularity,
            }

            url = self.api_url.format(symbol=get_ohlc_params.symbol)
            response = requests.get(url, params=params, timeout=TIMEOUT_SEC)
            data = response.json()

            if not data:
                break

            aggregated_data.extend(data)
            start_time = data[0][0] + granularity

            if chunk_end_time >= end_time:
                break

        return aggregated_data

    def convert_to_dataframe(self, aggregated_data: list) -> pd.DataFrame:
        df = pd.DataFrame(
            aggregated_data,
            columns=["Open time", "Low", "High", "Open", "Close", "Volume"],
        )
        df["Open time"] = pd.to_datetime(df["Open time"], unit="s")
        df.set_index("Open time", inplace=True)
        df.sort_index(inplace=True)

        return df
