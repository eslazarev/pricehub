""" Binance Broker ABC Class """

import requests
import pandas as pd

from pricehub.brokers.broker_abc import BrokerABC
from pricehub.config import TIMEOUT_SEC


class BrokerBinanceABC(BrokerABC):
    """
    Binance Broker  ABC Class
    """

    base_url = ""
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

    def get_ohlc(self, get_ohlc_params: "GetOhlcParams") -> pd.DataFrame:  # type: ignore[name-defined]
        self.validate_interval(get_ohlc_params)

        start_time = int(get_ohlc_params.start.timestamp() * 1000)
        end_time = int(get_ohlc_params.end.timestamp() * 1000)

        all_data = []

        while start_time < end_time:
            url = (
                f"{self.base_url}?symbol={get_ohlc_params.symbol}&interval={get_ohlc_params.interval}"
                f"&startTime={start_time}&endTime={end_time}"
            )
            data = requests.get(url, timeout=TIMEOUT_SEC).json()
            if not data:
                break
            all_data.extend(data)
            start_time = data[-1][0] + 1

        df = pd.DataFrame(
            all_data,
            columns=self.columns,
        )
        df = df.astype(float)
        df["Open time"] = pd.to_datetime(df["Open time"], unit="ms")
        df["Close time"] = pd.to_datetime(df["Close time"], unit="ms")
        df.set_index("Open time", inplace=True)

        return df
