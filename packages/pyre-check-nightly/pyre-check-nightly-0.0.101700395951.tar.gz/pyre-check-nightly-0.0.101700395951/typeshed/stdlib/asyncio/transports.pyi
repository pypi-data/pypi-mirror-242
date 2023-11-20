from asyncio.events import AbstractEventLoop
from asyncio.protocols import BaseProtocol
from collections.abc import Iterable, Mapping
from socket import _Address
from typing import Any

__all__ = ("BaseTransport", "ReadTransport", "WriteTransport", "Transport", "DatagramTransport", "SubprocessTransport")

class BaseTransport:
    def __init__(self, extra: Mapping[str, Any] | None = None) -> None: ...
    def get_extra_info(self, name: str, default: Any = None) -> Any: ...
    def is_closing(self) -> bool: ...
    def close(self) -> None: ...
    def set_protocol(self, protocol: BaseProtocol) -> None: ...
    def get_protocol(self) -> BaseProtocol: ...

class ReadTransport(BaseTransport):
    def is_reading(self) -> bool: ...
    def pause_reading(self) -> None: ...
    def resume_reading(self) -> None: ...

class WriteTransport(BaseTransport):
    def set_write_buffer_limits(self, high: int | None = None, low: int | None = None) -> None: ...
    def get_write_buffer_size(self) -> int: ...
    def get_write_buffer_limits(self) -> tuple[int, int]: ...
    def write(self, data: bytes | bytearray | memoryview) -> None: ...
    def writelines(self, list_of_data: Iterable[bytes | bytearray | memoryview]) -> None: ...
    def write_eof(self) -> None: ...
    def can_write_eof(self) -> bool: ...
    def abort(self) -> None: ...

class Transport(ReadTransport, WriteTransport): ...

class DatagramTransport(BaseTransport):
    def sendto(self, data: bytes | bytearray | memoryview, addr: _Address | None = None) -> None: ...
    def abort(self) -> None: ...

class SubprocessTransport(BaseTransport):
    def get_pid(self) -> int: ...
    def get_returncode(self) -> int | None: ...
    def get_pipe_transport(self, fd: int) -> BaseTransport | None: ...
    def send_signal(self, signal: int) -> None: ...
    def terminate(self) -> None: ...
    def kill(self) -> None: ...

class _FlowControlMixin(Transport):
    def __init__(self, extra: Mapping[str, Any] | None = None, loop: AbstractEventLoop | None = None) -> None: ...
