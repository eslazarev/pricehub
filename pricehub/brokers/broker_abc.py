""" Abstract base class for brokers """

from abc import ABC
import pandas as pd


class BrokerABC(ABC):
    """
    Abstract base class for brokers
    """

    def get_ohlc(self, get_ohlc_params: "GetOhlcParams") -> pd.DataFrame:  # type: ignore[name-defined]
        """
        Get OHLC data from the broker.
        :param get_ohlc_params:
        :return:
        """
        raise NotImplementedError
