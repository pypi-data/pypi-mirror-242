from typing import Any, Generic, TypeVar

T = TypeVar("T", bound=tuple[Any, ...])


class Concat(Generic[T]):
    pass
