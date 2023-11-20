import datetime
from collections.abc import Iterable
from typing import ClassVar
from typing_extensions import Self

from dateutil.relativedelta import relativedelta

from .__version__ import (
    __author__ as __author__,
    __copyright__ as __copyright__,
    __email__ as __email__,
    __license__ as __license__,
    __version__ as __version__,
)

class DateTimeRange:
    NOT_A_TIME_STR: ClassVar[str]
    start_time_format: str
    end_time_format: str
    is_output_elapse: bool
    separator: str
    def __init__(
        self,
        start_datetime: datetime.datetime | str | None = ...,
        end_datetime: datetime.datetime | str | None = ...,
        start_time_format: str = ...,
        end_time_format: str = ...,
    ) -> None: ...
    @classmethod
    def from_range_text(
        cls, range_text: str, separator: str = ..., start_time_format: str | None = ..., end_time_format: str | None = ...
    ) -> DateTimeRange: ...
    def __eq__(self, other: object) -> bool: ...
    def __ne__(self, other: object) -> bool: ...
    def __add__(self, other: datetime.timedelta) -> DateTimeRange: ...
    def __iadd__(self, other: datetime.timedelta) -> Self: ...
    def __sub__(self, other: datetime.timedelta) -> DateTimeRange: ...
    def __isub__(self, other: datetime.timedelta) -> Self: ...
    def __contains__(self, x: datetime.timedelta | datetime.datetime | DateTimeRange | str) -> bool: ...
    @property
    def start_datetime(self) -> datetime.datetime: ...
    @property
    def end_datetime(self) -> datetime.datetime: ...
    @property
    def timedelta(self) -> datetime.timedelta: ...
    def is_set(self) -> bool: ...
    def validate_time_inversion(self) -> None: ...
    def is_valid_timerange(self) -> bool: ...
    def is_intersection(self, x: DateTimeRange, intersection_threshold: datetime.timedelta | None = None) -> bool: ...
    def get_start_time_str(self) -> str: ...
    def get_end_time_str(self) -> str: ...
    def get_timedelta_second(self) -> float: ...
    def set_start_datetime(self, value: datetime.datetime | str | None, timezone: str | None = ...) -> None: ...
    def set_end_datetime(self, value: datetime.datetime | str | None, timezone: str | None = ...) -> None: ...
    def set_time_range(self, start: datetime.datetime | str | None, end: datetime.datetime | str | None) -> None: ...
    def range(self, step: datetime.timedelta | relativedelta) -> Iterable[datetime.datetime]: ...
    def intersection(self, x: DateTimeRange, intersection_threshold: datetime.timedelta | None = None) -> DateTimeRange: ...
    def encompass(self, x: DateTimeRange) -> DateTimeRange: ...
    def truncate(self, percentage: float) -> None: ...
    def split(self, separator: str | datetime.datetime) -> list[DateTimeRange]: ...
    def subtract(self, x: DateTimeRange) -> DateTimeRange: ...
