from _typeshed import Incomplete, StrPath
from collections.abc import Iterator
from datetime import datetime
from typing import IO

from openpyxl.chartsheet.chartsheet import Chartsheet
from openpyxl.styles.named_styles import NamedStyle
from openpyxl.workbook.child import _WorkbookChild
from openpyxl.workbook.defined_name import DefinedName
from openpyxl.worksheet._write_only import WriteOnlyWorksheet
from openpyxl.worksheet.worksheet import Worksheet

INTEGER_TYPES: Incomplete

class Workbook:
    template: bool
    path: str
    defined_names: Incomplete
    properties: Incomplete
    security: Incomplete
    shared_strings: Incomplete
    loaded_theme: Incomplete
    vba_archive: Incomplete
    is_template: bool
    code_name: Incomplete
    encoding: str
    iso_dates: Incomplete
    rels: Incomplete
    calculation: Incomplete
    views: Incomplete
    def __init__(self, write_only: bool = ..., iso_dates: bool = ...) -> None: ...
    @property
    def epoch(self) -> datetime: ...
    @epoch.setter
    def epoch(self, value: datetime) -> None: ...
    @property
    def read_only(self) -> bool: ...
    @property
    def data_only(self) -> bool: ...
    @property
    def write_only(self) -> bool: ...
    @property
    def excel_base_date(self) -> datetime: ...
    @property
    def active(self) -> _WorkbookChild | None: ...
    @active.setter
    def active(self, value: _WorkbookChild | int) -> None: ...
    def create_sheet(self, title: str | None = ..., index: int | None = ...): ...
    def move_sheet(self, sheet: Worksheet | str, offset: int = ...) -> None: ...
    def remove(self, worksheet: Worksheet) -> None: ...
    def remove_sheet(self, worksheet: Worksheet) -> None: ...
    def create_chartsheet(self, title: str | None = ..., index: int | None = ...) -> Chartsheet: ...
    def get_sheet_by_name(self, name: str) -> Worksheet: ...
    def __contains__(self, key: str) -> bool: ...
    def index(self, worksheet: Worksheet) -> int: ...
    def get_index(self, worksheet: Worksheet) -> int: ...
    def __getitem__(self, key: str) -> Worksheet: ...
    def __delitem__(self, key: str) -> None: ...
    def __iter__(self) -> Iterator[Worksheet]: ...
    def get_sheet_names(self) -> list[Worksheet]: ...
    @property
    def worksheets(self) -> list[Worksheet]: ...
    @property
    def chartsheets(self) -> list[Chartsheet]: ...
    @property
    def sheetnames(self) -> list[str]: ...
    def create_named_range(
        self, name: str, worksheet: Worksheet | None = ..., value: str | Incomplete | None = ..., scope: Incomplete | None = ...
    ) -> None: ...
    def add_named_style(self, style: NamedStyle) -> None: ...
    @property
    def named_styles(self) -> list[str]: ...
    def get_named_ranges(self) -> list[DefinedName] | tuple[DefinedName, ...]: ...
    def add_named_range(self, named_range: DefinedName) -> None: ...
    def get_named_range(self, name: str) -> DefinedName: ...
    def remove_named_range(self, named_range: DefinedName) -> None: ...
    @property
    def mime_type(self) -> str: ...
    def save(self, filename: StrPath | IO[bytes]) -> None: ...
    @property
    def style_names(self) -> list[str]: ...
    def copy_worksheet(self, from_worksheet: Worksheet) -> Worksheet | WriteOnlyWorksheet: ...
    def close(self) -> None: ...
