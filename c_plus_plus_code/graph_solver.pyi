"""
Быстрая Дейкстра
"""
from __future__ import annotations
import collections.abc
import typing
__all__: list[str] = ['get_distances']
def get_distances(graph: collections.abc.Mapping[typing.SupportsInt | typing.SupportsIndex, collections.abc.Sequence[tuple[typing.SupportsInt | typing.SupportsIndex, typing.SupportsFloat | typing.SupportsIndex]]], start: typing.SupportsInt | typing.SupportsIndex, end: typing.SupportsInt | typing.SupportsIndex) -> float:
    """
    Нахождение дистанции
    """
