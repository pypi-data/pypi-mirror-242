from _typeshed import Incomplete
from typing import NoReturn

from stripe.api_resources.abstract import UpdateableAPIResource as UpdateableAPIResource
from stripe.api_resources.transfer import Transfer as Transfer

class Reversal(UpdateableAPIResource):
    OBJECT_NAME: str
    def instance_url(self) -> str: ...
    @classmethod
    def modify(cls, sid, **params) -> NoReturn: ...
    @classmethod
    def retrieve(cls, id, api_key: Incomplete | None = ..., **params) -> NoReturn: ...
