"""Validated request model for OHLC fetches."""

from typing import Any

import arrow
from pydantic import BaseModel, field_validator, model_validator, ConfigDict

from pricehub.models import Interval


class GetOhlcParams(BaseModel):
    """Validated parameters for a single OHLC fetch request.

    All public timestamp inputs are coerced to :class:`arrow.Arrow` so broker
    implementations can rely on a single time type. ``broker`` is coerced to
    the :class:`~pricehub.models.broker.Broker` enum by Pydantic.

    :ivar broker: Broker enum member identifying exchange and market.
    :ivar symbol: Native exchange symbol (e.g. ``"BTCUSDT"``, ``"BTC-USDT"``).
    :ivar interval: Candle interval as one of the supported
        :data:`~pricehub.models.types_common.Interval` literals.
    :ivar start: Inclusive window start as :class:`arrow.Arrow` (UTC).
    :ivar end: Exclusive window end as :class:`arrow.Arrow` (UTC).
    """

    broker: "Broker"  # type: ignore[name-defined]
    symbol: str
    interval: Interval
    start: arrow.Arrow
    end: arrow.Arrow

    model_config = ConfigDict(arbitrary_types_allowed=True)

    @field_validator("start", "end", mode="before")
    def convert_to_arrow(cls, value: Any) -> arrow.Arrow:
        """Coerce a loose timestamp value to :class:`arrow.Arrow`.

        Accepts integers/floats (Unix seconds or milliseconds), ISO 8601
        strings, ``datetime``, ``pandas.Timestamp``, or pre-built
        :class:`arrow.Arrow` instances.

        :param value: Raw timestamp input.
        :returns: Equivalent :class:`arrow.Arrow` in UTC.
        :raises ValueError: If ``value`` cannot be parsed as a timestamp.
        """
        try:
            return arrow.get(value)
        except Exception as e:
            raise ValueError(f"Invalid date format for value '{value}': {e}") from e

    @model_validator(mode="after")
    def check_start_before_end(self) -> "GetOhlcParams":
        """Ensure ``start`` precedes ``end``.

        :returns: ``self`` if the ordering is valid.
        :raises ValueError: If ``start`` is greater than ``end``.
        """
        if self.start > self.end:
            raise ValueError("The 'start' date must be before the 'end' date.")
        return self
