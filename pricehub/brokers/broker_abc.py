""" Abstract base class for brokers """

from abc import ABC, abstractmethod
import pandas as pd


class BrokerABC(ABC):
    """
    Abstract base class for brokers
    """

    @property
    @abstractmethod
    def interval_map(self) -> dict:
        """
        Mapping of intervals supported by the broker.
        :return: dictionary of intervals
        """

    @property
    @abstractmethod
    def columns(self) -> list:
        """
        Columns for the DataFrame.
        :return:
        """

    @property
    @abstractmethod
    def api_url(self) -> str:
        """
        API URL for the broker.
        :return:
        """

    def get_ohlc(self, get_ohlc_params: "GetOhlcParams") -> pd.DataFrame:  # type: ignore[name-defined]
        """
        Get OHLC data from the broker.
        :param get_ohlc_params:
        :return:
        """
        self.validate_interval(get_ohlc_params)
        aggregated_data = self.fetch_data(get_ohlc_params)
        df = self.convert_to_dataframe(aggregated_data)
        return df

    def validate_interval(self, get_ohlc_params: "GetOhlcParams") -> None:  # type: ignore[name-defined]
        """
        Validate the interval for the given broker.
        :param get_ohlc_params:
        :return:
        """
        interval = self.interval_map.get(get_ohlc_params.interval)
        broker_name = self.__class__.__name__
        if not interval:
            raise ValueError(
                f"Interval '{get_ohlc_params.interval}' is not supported by {broker_name}."
                f"Supported intervals: {list(self.interval_map.keys())}"
            )

    @abstractmethod
    def fetch_data(self, get_ohlc_params: "GetOhlcParams") -> list:  # type: ignore[name-defined]
        """
        Fetch data from the broker.
        :param get_ohlc_params:
        :return:
        """

    @abstractmethod
    def convert_to_dataframe(self, aggregated_data: list) -> pd.DataFrame:
        """
        Convert the fetched data to a DataFrame.
        :param aggregated_data:
        :return:
        """
