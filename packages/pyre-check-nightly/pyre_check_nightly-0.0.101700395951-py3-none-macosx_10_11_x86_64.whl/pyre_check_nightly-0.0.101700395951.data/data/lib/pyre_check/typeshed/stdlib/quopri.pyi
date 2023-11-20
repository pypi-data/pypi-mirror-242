from _typeshed import ReadableBuffer, SupportsNoArgReadline, SupportsRead, SupportsWrite
from typing import Protocol

__all__ = ["encode", "decode", "encodestring", "decodestring"]

class _Input(SupportsRead[bytes], SupportsNoArgReadline[bytes], Protocol): ...

def encode(input: _Input, output: SupportsWrite[bytes], quotetabs: int, header: bool = False) -> None: ...
def encodestring(s: ReadableBuffer, quotetabs: bool = False, header: bool = False) -> bytes: ...
def decode(input: _Input, output: SupportsWrite[bytes], header: bool = False) -> None: ...
def decodestring(s: str | ReadableBuffer, header: bool = False) -> bytes: ...
