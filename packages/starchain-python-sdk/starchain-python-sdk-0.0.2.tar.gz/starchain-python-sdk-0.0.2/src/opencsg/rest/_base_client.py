import httpx
from httpx import URL
from ._constants import (
    DEFAULT_MAX_RETRIES,
    DEFAULT_TIMEOUT,
)
import json
import email.utils
import email
from random import random
import time
import logging
from typing import (
    TYPE_CHECKING,
    Mapping,
    TypeVar,
    Type,
    Optional,
    cast,
    Any,
    Union,
    Dict,
)
from types import TracebackType
from ._type import FinalRequestOptions, ResponseT, Omit, NotGiven, Headers, Body, RequestOptions
from ._exceptions import APITimeoutError, APIConnectionError, APIStatusError


if TYPE_CHECKING:
    from httpx._config import DEFAULT_TIMEOUT_CONFIG as HTTPX_DEFAULT_TIMEOUT
else:
    try:
        from httpx._config import DEFAULT_TIMEOUT_CONFIG as HTTPX_DEFAULT_TIMEOUT
    except ImportError:
        # taken from https://github.com/encode/httpx/blob/3ba5fe0d7ac70222590e759c31442b1cab263791/httpx/_config.py#L366
        HTTPX_DEFAULT_TIMEOUT = Timeout(5.0)

_T = TypeVar("_T")
_T_co = TypeVar("_T_co", covariant=True)
log: logging.Logger = logging.getLogger(__name__)


def _merge_mappings(
    obj1: Mapping[_T_co, Union[_T, Omit]],
    obj2: Mapping[_T_co, Union[_T, Omit]],
) -> Dict[_T_co, _T]:
    """Merge two mappings of the same type, removing any values that are instances of `Omit`.

    In cases with duplicate keys the second mapping takes precedence.
    """
    merged = {**obj1, **obj2}
    return {key: value for key, value in merged.items() if not isinstance(value, Omit)}

class SyncAPIClient():
    _client: httpx.Client
    _has_custom_http_client: bool

    def __init__(
        self,
        *,
        base_url: str | URL,
        max_retries: int = DEFAULT_MAX_RETRIES,
        timeout: float | None = None,
        http_client: httpx.Client | None = None,
        custom_headers: Mapping[str, str] | None = None,
        custom_query: Mapping[str, object] | None = None,
    ) -> None:
        if not timeout:
            # if the user passed in a custom http client with a non-default
            # timeout set then we use that timeout.
            #
            # note: there is an edge case here where the user passes in a client
            # where they've explicitly set the timeout to match the default timeout
            # as this check is structural, meaning that we'll think they didn't
            # pass in a timeout and will ignore it
            if http_client and http_client.timeout != HTTPX_DEFAULT_TIMEOUT:
                timeout = http_client.timeout
            else:
                timeout = DEFAULT_TIMEOUT

        self._client = http_client or httpx.Client(
            base_url=base_url,
            # cast to a valid type because mypy doesn't understand our type narrowing
            timeout=timeout,
        )
        self.timeout = timeout
        self._custom_query = custom_query or {}
        self._custom_headers = custom_headers or {}
        self.max_retries = max_retries
        self._base_url = self._enforce_trailing_slash(URL(base_url))

    def _enforce_trailing_slash(self, url: URL) -> URL:
        if url.raw_path.endswith(b"/"):
            return url
        return url.copy_with(raw_path=url.raw_path + b"/")
    
    def _prepare_options(
        self,
        options: FinalRequestOptions,  # noqa: ARG002
    ) -> None:
        """Hook for mutating the given options"""
        return None

    def _prepare_request(
        self,
        request: httpx.Request,  # noqa: ARG002
    ) -> None:
        """This method is used as a callback for mutating the `Request` object
        after it has been constructed.
        This is useful for cases where you want to add certain headers based off of
        the request properties, e.g. `url`, `method` etc.
        """
        return None

    def _remaining_retries(
        self,
        remaining_retries: Optional[int],
        options: FinalRequestOptions,
    ) -> int:
        return remaining_retries if remaining_retries is not None else options.get_max_retries(self.max_retries)


    def _prepare_url(self, url: str) -> URL:
        """
        Merge a URL argument together with any 'base_url' on the client,
        to create the URL used for the outgoing request.
        """
        # Copied from httpx's `_merge_url` method.
        merge_url = URL(url)
        if merge_url.is_relative_url:
            merge_raw_path = self.base_url.raw_path + merge_url.raw_path.lstrip(b"/")
            return self.base_url.copy_with(raw_path=merge_raw_path)

        return merge_url
    
    def _validate_headers(
        self,
        headers: Headers,  # noqa: ARG002
        custom_headers: Headers,  # noqa: ARG002
    ) -> None:
        """Validate the given default headers and custom headers.

        Does nothing by default.
        """
        return
       
    def _build_headers(self, options: FinalRequestOptions) -> httpx.Headers:
        custom_headers = options.headers or {}
        headers_dict = _merge_mappings(self.default_headers, custom_headers)
        self._validate_headers(headers_dict, custom_headers)

        headers = httpx.Headers(headers_dict)

        return headers
    
    def _build_request(
        self,
        options: FinalRequestOptions,
    ) -> httpx.Request:
        if log.isEnabledFor(logging.DEBUG):
            log.debug("Request options: %s", options)

        kwargs: dict[str, Any] = {}

        json_data = options.json_data

        headers = self._build_headers(options)
        params = _merge_mappings(self._custom_query, options.params)

        # TODO: report this error to httpx
        return self._client.build_request(  # pyright: ignore[reportUnknownMemberType]
            headers=headers,
            timeout=self.timeout if isinstance(options.timeout, NotGiven) else options.timeout,
            method=options.method,
            url=self._prepare_url(options.url),
            # the `Query` type that we use is incompatible with qs'
            # `Params` type as it needs to be typed as `Mapping[str, object]`
            # so that passing a `TypedDict` doesn't cause an error.
            # https://github.com/microsoft/pyright/issues/3526#event-6715453066
            json=json_data,
            **kwargs,
        )

    def _should_retry(self, response: httpx.Response) -> bool:
        # Note: this is not a standard header
        should_retry_header = response.headers.get("x-should-retry")

        # If the server explicitly says whether or not to retry, obey.
        if should_retry_header == "true":
            return True
        if should_retry_header == "false":
            return False

        # Retry on request timeouts.
        if response.status_code == 408:
            return True

        # Retry on lock timeouts.
        if response.status_code == 409:
            return True

        # Retry on rate limits.
        if response.status_code == 429:
            return True

        # Retry internal errors.
        if response.status_code >= 500:
            return True

        return False
    
    def request(
        self,
        cast_to: Type[ResponseT],
        options: FinalRequestOptions,
        remaining_retries: Optional[int] = None,
    ) -> ResponseT:
        return self._request(
            cast_to=cast_to,
            options=options,
            remaining_retries=remaining_retries,
        )

    def _request(
        self,
        *,
        cast_to: Type[ResponseT],
        options: FinalRequestOptions,
        remaining_retries: int | None,
    ) -> ResponseT:
        self._prepare_options(options)
        retries = self._remaining_retries(remaining_retries, options)
        request = self._build_request(options)
        self._prepare_request(request)

        try:
            response = self._client.send(request, auth=self.custom_auth)
            log.debug(
                'HTTP Request: %s %s "%i %s"', request.method, request.url, response.status_code, response.reason_phrase
            )
            response.raise_for_status()
        except httpx.HTTPStatusError as err:  # thrown on 4xx and 5xx status code
            if retries > 0 and self._should_retry(err.response):
                return self._retry_request(
                    options,
                    cast_to,
                    retries,
                    err.response.headers,
                )

            # If the response is streamed then we need to explicitly read the response
            # to completion before attempting to access the response text.
            err.response.read()
            raise self._make_status_error_from_response(err.response) from None
        except httpx.TimeoutException as err:
            if retries > 0:
                return self._retry_request(
                    options,
                    cast_to,
                    retries,
                )
            raise APITimeoutError(request=request) from err
        except Exception as err:
            if retries > 0:
                return self._retry_request(
                    options,
                    cast_to,
                    retries,
                )
            raise APIConnectionError(request=request) from err

        return self._process_response(
            cast_to=cast_to,
            options=options,
            response=response,
        )

    def _make_status_error_from_response(
        self,
        response: httpx.Response,
    ) -> APIStatusError:
        err_text = response.text.strip()
        body = err_text

        try:
            body = json.loads(err_text)
            err_msg = f"Error code: {response.status_code} - {body}"
        except Exception:
            err_msg = err_text or f"Error code: {response.status_code}"

        return self._make_status_error(err_msg, body=body, response=response)

    def _make_status_error(
        self,
        err_msg: str,
        *,
        body: object,
        response: httpx.Response,
    ) -> APIStatusError:
        raise NotImplementedError()
    
    def _calculate_retry_timeout(
        self,
        remaining_retries: int,
        options: FinalRequestOptions,
        response_headers: Optional[httpx.Headers] = None,
    ) -> float:
        max_retries = options.get_max_retries(self.max_retries)
        try:
            # About the Retry-After header: https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Retry-After
            #
            # <http-date>". See https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Retry-After#syntax for
            # details.
            if response_headers is not None:
                retry_header = response_headers.get("retry-after")
                try:
                    retry_after = int(retry_header)
                except Exception:
                    retry_date_tuple = email.utils.parsedate_tz(retry_header)
                    if retry_date_tuple is None:
                        retry_after = -1
                    else:
                        retry_date = email.utils.mktime_tz(retry_date_tuple)
                        retry_after = int(retry_date - time.time())
            else:
                retry_after = -1

        except Exception:
            retry_after = -1

        # If the API asks us to wait a certain amount of time (and it's a reasonable amount), just do what it says.
        if 0 < retry_after <= 60:
            return retry_after

        initial_retry_delay = 0.5
        max_retry_delay = 8.0
        nb_retries = max_retries - remaining_retries

        # Apply exponential backoff, but not more than the max.
        sleep_seconds = min(initial_retry_delay * pow(2.0, nb_retries), max_retry_delay)

        # Apply some jitter, plus-or-minus half a second.
        jitter = 1 - 0.25 * random()
        timeout = sleep_seconds * jitter
        return timeout if timeout >= 0 else 0
    
    def _retry_request(
        self,
        options: FinalRequestOptions,
        cast_to: Type[ResponseT],
        remaining_retries: int,
        response_headers: Optional[httpx.Headers] = None,
    ) -> ResponseT:
        remaining = remaining_retries - 1
        timeout = self._calculate_retry_timeout(remaining, options, response_headers)
        log.info("Retrying request to %s in %f seconds", options.url, timeout)

        # In a synchronous context we are blocking the entire thread. Up to the library user to run the client in a
        # different thread if necessary.
        time.sleep(timeout)

        return self._request(
            options=options,
            cast_to=cast_to,
            remaining_retries=remaining,
        )
    
    def _process_response(
        self,
        *,
        cast_to: Type[ResponseT],
        options: FinalRequestOptions,
        response: httpx.Response,
    ) -> ResponseT:
        return response.text
    
    def post(
        self,
        path: str,
        *,
        cast_to: Type[ResponseT],
        body: Body | None = None,
        options: RequestOptions = {},
    ) -> ResponseT:
        opts = FinalRequestOptions.construct(
            method="post", url=path, json_data=body, **options
        )
        return cast(ResponseT, self.request(cast_to, opts))


    def delete(
        self,
        path: str,
        *,
        cast_to: Type[ResponseT],
        body: Body | None = None,
        options: RequestOptions = {},
    ) -> ResponseT:
        opts = FinalRequestOptions.construct(method="delete", url=path, json_data=body, **options)
        return self.request(cast_to, opts)

    def is_closed(self) -> bool:
        return self._client.is_closed

    def close(self) -> None:
        """Close the underlying HTTPX client.

        The client will *not* be usable after this.
        """
        # If an error is thrown while constructing a client, self._client
        # may not be present
        if hasattr(self, "_client"):
            self._client.close()

    def __enter__(self: _T) -> _T:
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        self.close()

    @property
    def auth_headers(self) -> dict[str, str]:
        return {}
    
    
    @property
    def default_headers(self) -> dict[str, str | Omit]:
        return {
            "Accept": "application/json",
            "Content-Type": "application/json",
            **self.auth_headers,
            **self._custom_headers,
        }
    
    @property
    def custom_auth(self) -> httpx.Auth | None:
        return None

    @property
    def base_url(self) -> URL:
        return self._base_url