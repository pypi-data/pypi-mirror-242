from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ._client import StarChain

class SyncAPIResource:
    _client: StarChain

    def __init__(self, client: StarChain) -> None:
        self._client = client
        self._post = client.post