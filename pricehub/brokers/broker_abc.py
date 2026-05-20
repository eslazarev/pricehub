"""Abstract base class shared by all broker implementations."""

from abc import ABC, abstractmethod
import pandas as pd


class BrokerABC(ABC):
    """Abstract contract every broker implementation must satisfy.

    A concrete broker provides three pieces of metadata (``api_url``,
    ``columns``, ``interval_map``) plus two behaviors:
    :meth:`fetch_data` (HTTP) and :meth:`convert_to_dataframe` (parsing).
    The template :meth:`get_ohlc` wires these together with interval
    validation. Brokers must be stateless — instances are created per call.
    """

    @property
    @abstractmethod
    def interval_map(self) -> dict:
        """Mapping from pricehub interval strings to broker-native codes.

        Keys are pricehub-canonical intervals (e.g. ``"1h"``, ``"1d"``).
        Values are whatever the exchange API expects (e.g. ``60``, ``"1day"``).
        Only intervals present in this mapping are accepted.
        """

    @property
    @abstractmethod
    def columns(self) -> list:
        """Ordered list of DataFrame column names produced by this broker.

        The first column is always ``"Open time"`` and is used as the index
        after conversion. Remaining columns mirror upstream API field names.
        """

    @property
    @abstractmethod
    def api_url(self) -> str:
        """Base URL of the exchange klines/candles endpoint."""

    def get_ohlc(self, get_ohlc_params: "GetOhlcParams") -> pd.DataFrame:  # type: ignore[name-defined]
        """Template method: validate, fetch, and convert to DataFrame.

        :param get_ohlc_params: Validated request parameters.
        :returns: OHLC data as a :class:`pandas.DataFrame`.
        :raises ValueError: If the interval is unsupported by this broker.
        """
        self.validate_interval(get_ohlc_params)
        aggregated_data = self.fetch_data(get_ohlc_params)
        df = self.convert_to_dataframe(aggregated_data)
        return df

    def validate_interval(self, get_ohlc_params: "GetOhlcParams") -> None:  # type: ignore[name-defined]
        """Check that the requested interval is supported by this broker.

        :param get_ohlc_params: Request parameters carrying the interval.
        :raises ValueError: If the interval is not in :attr:`interval_map`.
            The error message lists all supported intervals to aid debugging.
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
        """Fetch raw candle rows from the exchange API, paginating as needed.

        Implementations are responsible for handling exchange-specific
        pagination cursors, deduplication across overlapping pages, and
        translating HTTP errors into :class:`requests.HTTPError`.

        :param get_ohlc_params: Validated request parameters.
        :returns: List of rows in the order expected by :attr:`columns`.
        """

    @abstractmethod
    def convert_to_dataframe(self, aggregated_data: list) -> pd.DataFrame:
        """Convert raw broker rows into a typed DataFrame indexed by time.

        :param aggregated_data: Output of :meth:`fetch_data`.
        :returns: DataFrame with columns matching :attr:`columns`, indexed
            on UTC ``Open time``.
        """
