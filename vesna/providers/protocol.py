import pathlib
import typing
from typing import Protocol


class ProviderProtocol(Protocol):
    """
    Provides a basic protocol for providers that will be compatible with Vesna.
    """

    @classmethod
    async def from_file(cls, path: pathlib.Path, locale_code: str) -> ProviderProtocol: ...

    def __getitem__(self, key: str) -> str | None: ...

    def __setitem__(self, key: str, value: str) -> str: ...

    def get(self, key: str, default: str | None = None, **kwargs) -> str | None: ...

    def set(self, key: str, value: str) -> str: ...

    def get_storage(self) -> ModelDataProtocol: ...

    def get_locale_code(self) -> str | None: ...

    def get_file_path(self) -> pathlib.Path | None: ...

    async def load_file(self, path: pathlib.Path, locale_code: str) -> None: ...

    async def save_file(self, path: pathlib.Path | None = None) -> None: ...

    async def clean(self) -> None: ...

    def is_empty(self) -> bool: ...


class ModelDataProtocol(Protocol):
    """
    Provides a base protocol for a model that will be compatible with ProviderProtocol.
    """

    data: typing.Any
    locale_code: str | None  # ISO 15897 (ISO 639-1 + ISO 3166-1 alpha-2)

    path: pathlib.Path | None = None

    version: str
