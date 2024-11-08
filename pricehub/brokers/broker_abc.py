""" Abstract base class for brokers """

from abc import ABC, abstractmethod
import pandas as pd


class BrokerABC(ABC):
    """
    Abstract base class for brokers
    """

    interval_map: dict = {}

    @abstractmethod
    def get_ohlc(self, get_ohlc_params: "GetOhlcParams") -> pd.DataFrame:  # type: ignore[name-defined]
        """
        Get OHLC data from the broker.
        :param get_ohlc_params:
        :return:
        """
        raise NotImplementedError

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
