from abc import ABC, abstractmethod
import json
from typing import Any, Generic, TypeVar

from merrymake.contenttype import _ContentType, ContentType

# Define a generic type variable
T = TypeVar('T')

# Define a protocol for the ValueMapper
class ValueMapper(Generic[T],ABC):
    @abstractmethod
    def is_none(self) -> T:
        pass
    @abstractmethod
    def is_bytes(self, buf: bytes) -> T:
        pass
    @abstractmethod
    def is_string(self, buf: str) -> T:
        pass
    @abstractmethod
    def is_dict(self, buf: dict[str,Any]) -> T:
        pass

# Define the valueTo function
def value_to(value: None | bytes | str | dict[str,Any], map: ValueMapper[T]) -> T:
    if value is None:
        return map.is_none()
    elif type(value) is str:
        return map.is_string(value)
    elif type(value) is bytes:
        return map.is_bytes(value)
    elif type(value) is dict:
        return map.is_dict(value)
    else:
        raise TypeError("Unsupported type")

class StringValueMapper(ValueMapper[str]):
    def is_none(self) -> str:
        return "None"
    def is_bytes(self, buf: bytes) -> str:
        return buf.decode("utf-8")
    def is_string(self, buf: str) -> str:
        return buf
    def is_dict(self, buf: dict[str,Any]) -> str:
        return json.dumps(buf)
class BytesValueMapper(ValueMapper[bytes]):
    def is_none(self) -> bytes:
        return bytes()
    def is_bytes(self, buf: bytes) -> bytes:
        return buf
    def is_string(self, buf: str) -> bytes:
        return bytes(buf, "utf-8")
    def is_dict(self, buf: dict[str,Any]) -> bytes:
        return bytes(json.dumps(buf), "utf-8")
class ContentTypeValueMapper(ValueMapper[_ContentType | None]):
    def is_none(self) -> None:
        return None
    def is_bytes(self, buf: bytes) -> _ContentType:
        return ContentType.raw
    def is_string(self, buf: str) -> _ContentType:
        return ContentType.text
    def is_dict(self, buf: dict[str,Any]) -> _ContentType:
        return ContentType.json

A = TypeVar('A')
B = TypeVar('B')

class Both(ValueMapper[tuple[A,B]]):
    _a: ValueMapper[A]
    _b: ValueMapper[B]
    def __init__(self, a: ValueMapper[A], b: ValueMapper[B]) -> None:
        self._a = a
        self._b = b
    def is_none(self) -> tuple[A,B]:
        return (self._a.is_none(), self._b.is_none())
    def is_bytes(self, buf: bytes) -> tuple[A,B]:
        return (self._a.is_bytes(buf), self._b.is_bytes(buf))
    def is_string(self, buf: str) -> tuple[A,B]:
        return (self._a.is_string(buf), self._b.is_string(buf))
    def is_dict(self, buf: dict[str,Any]) -> tuple[A,B]:
        return (self._a.is_dict(buf), self._b.is_dict(buf))

class to:
    String = StringValueMapper()
    Bytes = BytesValueMapper()
    ContentType = ContentTypeValueMapper()
