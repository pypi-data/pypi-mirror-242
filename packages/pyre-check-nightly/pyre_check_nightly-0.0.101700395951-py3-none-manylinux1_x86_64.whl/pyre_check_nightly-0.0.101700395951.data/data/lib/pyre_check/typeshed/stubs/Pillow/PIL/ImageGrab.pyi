from _typeshed import Incomplete

from .Image import Image, _Box

def grab(
    bbox: _Box | None = ..., include_layered_windows: bool = ..., all_screens: bool = ..., xdisplay: Incomplete | None = ...
) -> Image: ...
def grabclipboard() -> Image | None: ...
