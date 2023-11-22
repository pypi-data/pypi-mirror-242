from __future__ import annotations

import pydantic
from typing import (
    TYPE_CHECKING,
    List, 
    Optional, 
    Mapping,
    Union,
    TypeVar,
    Any,
    cast,
    Dict,
)

PYDANTIC_V2 = pydantic.VERSION.startswith("2.")
if TYPE_CHECKING:
    from pydantic import ConfigDict as ConfigDict
else:
    if PYDANTIC_V2:
        from pydantic import ConfigDict
    else:
        # TODO: provide an error message here?
        ConfigDict = None

from typing_extensions import (
    Unpack,
    final,
    Literal,
    override,
    Required,
    TypedDict,
    runtime_checkable,
    Protocol,
    ClassVar,
)

from ._utils import (
    is_given,
    strip_not_given,
)

from ._base_type import NotGiven

from httpx import URL, Proxy, Timeout, Response, BaseTransport, AsyncBaseTransport

# Sentinel class used when the response type is an object with an unknown schema
class UnknownResponse:
    ...

Body = object
_T = TypeVar("_T")
@runtime_checkable
class ModelBuilderProtocol(Protocol):
    @classmethod
    def build(
        cls: type[_T],
        *,
        response: Response,
        data: object,
    ) -> _T:
        ...

ResponseT = TypeVar(
    "ResponseT",
    bound="Union[str, None, List[Any], Dict[str, Any], Response, UnknownResponse, ModelBuilderProtocol]",
)

class Omit:
    """In certain situations you need to be able to represent a case where a default value has
    to be explicitly removed and `None` is not an appropriate substitute, for example:

    ```py
    # as the default `Content-Type` header is `application/json` that will be sent
    client.post('/upload/files', files={'file': b'my raw file content'})

    # you can't explicitly override the header as it has to be dynamically generated
    # to look something like: 'multipart/form-data; boundary=0d8382fcf5f8c3be01ca2e11002d2983'
    client.post(..., headers={'Content-Type': 'multipart/form-data'})

    # instead you can remove the default `application/json` header by passing Omit
    client.post(..., headers={'Content-Type': Omit()})
    ```
    """

    def __bool__(self) -> Literal[False]:
        return False



_T = TypeVar("_T")
Query = Mapping[str, object]
Headers = Mapping[str, Union[str, Omit]]

__all__ = ["Completion"]


    
class ChatflowUsage(pydantic.BaseModel):
    completion_tokens: int
    """Number of tokens in the generated completion."""

    prompt_tokens: int
    """Number of tokens in the prompt."""

    total_tokens: int
    """Total number of tokens used in the request (prompt + completion)."""

class ChatflowChoice(pydantic.BaseModel):
    message: str

class Chatflow(pydantic.BaseModel):
    id: str
    """A unique identifier for the completion."""

    choices: List[ChatflowChoice]
    """The list of completion choices the model generated for the input prompt."""

    created: int
    """The Unix timestamp (in seconds) of when the completion was created."""

    chatflowID: str
    """The model used for completion."""


    usage: Optional[ChatflowUsage] = None
    """Usage statistics for the completion request."""

class FinalRequestOptionsInput(TypedDict, total=False):
    method: Required[str]
    url: Required[str]
    params: Query
    headers: Headers
    max_retries: int
    timeout: float | None
    json_data: Body

@final
class FinalRequestOptions(pydantic.BaseModel):
    method: str
    url: str
    params: Query = {}
    headers: Union[Headers, NotGiven] = NotGiven()
    max_retries: Union[int, NotGiven] = NotGiven()
    timeout: Union[float, None, NotGiven] = NotGiven()
    # It should be noted that we cannot use `json` here as that would override
    # a BaseModel method in an incompatible fashion.
    json_data: Union[Body, None] = None
    if PYDANTIC_V2:
        model_config: ClassVar[ConfigDict] = ConfigDict(arbitrary_types_allowed=True)
    else:

        class Config(pydantic.BaseConfig):  # pyright: ignore[reportDeprecated]
            arbitrary_types_allowed: bool = True

    def get_max_retries(self, max_retries: int) -> int:
        if isinstance(self.max_retries, NotGiven):
            return max_retries
        return self.max_retries

    # override the `construct` method so that we can run custom transformations.
    # this is necessary as we don't want to do any actual runtime type checking
    # (which means we can't use validators) but we do want to ensure that `NotGiven`
    # values are not present
    #
    # type ignore required because we're adding explicit types to `**values`
    @classmethod
    def construct(  # type: ignore
        cls,
        _fields_set: set[str] | None = None,
        **values: Unpack[FinalRequestOptionsInput],
    ) -> FinalRequestOptions:
        kwargs: dict[str, Any] = {
            # we unconditionally call `strip_not_given` on any value
            # as it will just ignore any non-mapping types
            key: strip_not_given(value)
            for key, value in values.items()
        }

        return cast(FinalRequestOptions, super().construct(_fields_set, **kwargs))  # pyright: ignore[reportDeprecated]

class RequestOptions(TypedDict, total=False):
    headers: Headers
    max_retries: int
    timeout: float | Timeout | None
    params: Query

Headers = Mapping[str, Union[str, Omit]]