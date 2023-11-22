from __future__ import annotations
from .._resource import SyncAPIResource
from typing import TYPE_CHECKING
from .._type import Body

if TYPE_CHECKING:
    from .._client import StarChain


__all__ = [
    "Chatflows"
]

class Chatflows(SyncAPIResource):
    id: str

    def __init__(
        self, 
        client: StarChain):
        """
        Initialize the ChatFlow
        """
        super().__init__(client)  
    
    def run(
        self,
        *,
        id: str,
        message: Body
        ):
        """
        TODO
        """
        path = "/prediction/" + id
        return self._post(
                path,
                cast_to=None,
                body = message
            )
