from _typeshed import Incomplete

class Ready:
    openapi_types: Incomplete
    attribute_map: Incomplete
    discriminator: Incomplete
    def __init__(
        self, status: Incomplete | None = ..., started: Incomplete | None = ..., up: Incomplete | None = ...
    ) -> None: ...
    @property
    def status(self): ...
    @status.setter
    def status(self, status) -> None: ...
    @property
    def started(self): ...
    @started.setter
    def started(self, started) -> None: ...
    @property
    def up(self): ...
    @up.setter
    def up(self, up) -> None: ...
    def to_dict(self): ...
    def to_str(self): ...
    def __eq__(self, other): ...
    def __ne__(self, other): ...
