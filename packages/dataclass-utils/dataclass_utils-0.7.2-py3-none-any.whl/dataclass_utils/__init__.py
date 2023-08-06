r"""

# Example

## `check_type` function

>>> import dataclasses
>>> from typing import List
>>> @dataclasses.dataclass
... class Foo:
...     a: int
...     b: List[str]

>>> import pytest
>>> check_type(Foo(1, ["b"])) # OK
>>> with pytest.raises(TypeError):
...     check_type(Foo("a", [2]))

## `into_dataclass` function

Recursively constructs dataclass from dict

>>> @dataclasses.dataclass
... class Foo:
...     a: int
>>> @dataclasses.dataclass
... class Bar:
...     foo: Foo
...     b: str
>>> data = {"foo": {"a": 1}, "b": "foo"}
>>> bar = into_dataclass(Bar, data)
>>> assert bar.foo == Foo(**data["foo"]) # field `foo` is instantiated as `Foo`, not dict
"""

from typing import Type, TypeVar

from dataclass_utils.type_checker import check_root as check_type
from dataclass_utils.into_dataclass import into_dataclass
from .VERSION import __version__

T = TypeVar("T")


__all__ = ["check_type", "into_dataclass", "__version__"]
