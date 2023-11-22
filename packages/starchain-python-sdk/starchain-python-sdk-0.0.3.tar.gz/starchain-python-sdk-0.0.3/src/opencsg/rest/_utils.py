from __future__ import annotations
from typing import TYPE_CHECKING, Union, Dict, TypeVar

from typing import (
    Mapping,
    overload,
)
from typing_extensions import TypeGuard, TypeVar
from ._base_type import NotGiven, NotGivenOr

_T = TypeVar("_T")
_K = TypeVar("_K")
_V = TypeVar("_V")

def is_given(obj: NotGivenOr[_T]) -> TypeGuard[_T]:
    return not isinstance(obj, NotGiven)

@overload
def strip_not_given(obj: None) -> None:
    ...


@overload
def strip_not_given(obj: Mapping[_K, _V | NotGiven]) -> dict[_K, _V]:
    ...


@overload
def strip_not_given(obj: object) -> object:
    ...


def is_mapping(obj: object) -> TypeGuard[Mapping[str, object]]:
    return isinstance(obj, Mapping)

def strip_not_given(obj: object | None) -> object:
    """Remove all top-level keys where their values are instances of `NotGiven`"""
    if obj is None:
        return None

    if not is_mapping(obj):
        return obj

    return {key: value for key, value in obj.items() if not isinstance(value, NotGiven)}