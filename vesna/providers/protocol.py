import pathlib

from typing import Protocol

class ProviderProtocol(Protocol):
    @classmethod
    async def from_file(cls, path: pathlib.Path, locale_code: str) -> ProviderProtocol:
        instance = cls()
        await instance.load_file(path, locale_code)
        return instance

    def __getitem__(self, key: str) -> str:
        pass

    def __setitem__(self, key: str, value: str) -> str:
        pass

    def get(self, key: str, default: str | None = None) -> str:
        pass

    def set(self, key: str, value: str) -> str:
        pass

    def get_locale_code(self) -> str | None:
        pass

    def get_file_path(self) -> pathlib.Path | None:
        pass

    async def load_file(self, path: pathlib.Path, locale_code: str) -> None:
        pass

    async def save_file(self, path: pathlib.Path | None = None) -> None:
        pass

    async def clean(self) -> None:
        pass

    def is_empty(self) -> bool:
        pass