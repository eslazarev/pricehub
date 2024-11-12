""" Binance Broker ABC Class """
from abc import ABC

import requests
import pandas as pd

from pricehub.brokers.broker_abc import BrokerABC
from pricehub.config import TIMEOUT_SEC


class BrokerBinanceABC(BrokerABC, ABC):
    """
    Binance Broker  ABC Class
    """

    columns = [
        "Open time",
        "Open",
        "High",
        "Low",
        "Close",
        "Volume",
        "Close time",
        "Quote asset volume",
        "Number of trades",
        "Taker buy base asset volume",
        "Taker buy quote asset volume",
        "Ignore",
    ]

    def fetch_data(self, get_ohlc_params: "GetOhlcParams") -> list:  # type: ignore[name-defined]
        """
        Implement the fetch_data method for Binance
        """

        start_time = int(get_ohlc_params.start.timestamp() * 1000)
        end_time = int(get_ohlc_params.end.timestamp() * 1000)

        aggregated_data: list = []

        while start_time < end_time:
            url = (
                f"{self.api_url}?symbol={get_ohlc_params.symbol}&interval={get_ohlc_params.interval}"
                f"&startTime={start_time}&endTime={end_time}"
            )
            data = requests.get(url, timeout=TIMEOUT_SEC).json()
            if not data:
                break
            aggregated_data.extend(data)
            start_time = data[-1][0] + 1

        return aggregated_data

    def convert_to_dataframe(self, aggregated_data: list) -> pd.DataFrame:
        """
        Implement the convert_to_dataframe method for Binance
        """
        df = pd.DataFrame(aggregated_data, columns=self.columns)
        df = df.astype(float)
        df["Open time"] = pd.to_datetime(df["Open time"], unit="ms")
        df["Close time"] = pd.to_datetime(df["Close time"], unit="ms")
        df.set_index("Open time", inplace=True)

        return df
