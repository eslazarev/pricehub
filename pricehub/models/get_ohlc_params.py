""" GetOhlcParams model. """

from typing import Any

import arrow
from pydantic import BaseModel, field_validator, model_validator, ConfigDict

from pricehub.models import Interval


class GetOhlcParams(BaseModel):
    """
    Get OHLC parameters.
    """

    broker: "Broker"  # type: ignore[name-defined]
    symbol: str
    interval: Interval
    start: arrow.Arrow
    end: arrow.Arrow

    model_config = ConfigDict(arbitrary_types_allowed=True)

    @field_validator("start", "end", mode="before")
    def convert_to_arrow(cls, value: Any) -> arrow.Arrow:
        """
        Convert the 'start' and 'end' values to Arrow objects.
        :param value:
        :return:
        """
        try:
            return arrow.get(value)
        except Exception as e:
            raise ValueError(f"Invalid date format for value '{value}': {e}") from e

    @model_validator(mode="after")
    def check_start_before_end(self) -> "GetOhlcParams":
        """
        Check that the 'start' date is before the 'end' date.
        :return:
        """
        if self.start > self.end:
            raise ValueError("The 'start' date must be before the 'end' date.")
        return self
