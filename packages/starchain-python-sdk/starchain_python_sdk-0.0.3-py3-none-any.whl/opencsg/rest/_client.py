import os
from .chatflow import Chatflows
from ._exceptions import StarChainError
from ._base_client import SyncAPIClient
import httpx
from ._constants import DEFAULT_MAX_RETRIES

__all__ = [
    "StarChain"
]

class StarChain(SyncAPIClient):
    """ 
    A client for accessing the hedera_mirror_sdk API. 
    """
    chatflows: Chatflows

    api_key: str
    organization: str | None
    base_url :  str

    def __init__(
        self, 
        *,
        api_key: str | None = None,
        organization: str | None = None,
        base_url: str | httpx.URL | None = None,
        timeout: float | None = None,
        max_retries: int = DEFAULT_MAX_RETRIES,
        ):

        """Construct a new synchronous starchain client instance.

        This automatically infers the following arguments from their corresponding environment variables if they are not provided:
        - `api_key` from `STARCHAIN_API_KEY`
        - `organization` from `STARCHAIN_ORG_ID`
        """
        if api_key is None:
            api_key = os.environ.get("STARCHAIN_API_KEY")
        if api_key is None:
            raise StarChainError(
                "The api_key client option must be set either by passing api_key to the client or by setting the STARCHAIN_API_KEY environment variable"
            )
        self.api_key = api_key

        if organization is None:
            organization = os.environ.get("STARCHAIN_ORG_ID")
        self.organization = organization       

        if base_url is None:
            base_url = os.environ.get("STARCHAIN_BASE_URL")
        if base_url is None:
            base_url = f"http://localhost:3000/api/v1"

        super().__init__(
            base_url=base_url,
            max_retries=max_retries,
            timeout=timeout,
        )

        self.chatflows = Chatflows(self)