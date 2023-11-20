from _typeshed import Incomplete

from influxdb_client.domain.view_properties import ViewProperties

class MarkdownViewProperties(ViewProperties):
    openapi_types: Incomplete
    attribute_map: Incomplete
    discriminator: Incomplete
    def __init__(self, type: Incomplete | None = ..., shape: Incomplete | None = ..., note: Incomplete | None = ...) -> None: ...
    @property
    def type(self): ...
    @type.setter
    def type(self, type) -> None: ...
    @property
    def shape(self): ...
    @shape.setter
    def shape(self, shape) -> None: ...
    @property
    def note(self): ...
    @note.setter
    def note(self, note) -> None: ...
    def to_dict(self): ...
    def to_str(self): ...
    def __eq__(self, other): ...
    def __ne__(self, other): ...
