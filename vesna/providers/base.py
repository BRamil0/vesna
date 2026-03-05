import pathlib

from abc import ABC, abstractmethod

class BaseProvider(ABC):
    @abstractmethod
    def __init__(self) -> None:
        pass

    @classmethod
    async def from_file(cls, path: pathlib.Path, locale_code: str) -> BaseProvider:
        instance = cls()
        await instance.load_file(path, locale_code)
        return instance

    @abstractmethod
    def __getitem__(self, key: str) -> str:
        pass

    @abstractmethod
    def __setitem__(self, key: str, value: str) -> str:
        pass

    @abstractmethod
    def get(self, key: str, default: str | None = None) -> str:
        pass

    @abstractmethod
    def set(self, key: str, value: str) -> str:
        pass

    @abstractmethod
    def get_locale_code(self) -> str | None:
        pass

    @abstractmethod
    def get_file_path(self) -> pathlib.Path | None:
        pass

    @abstractmethod
    async def load_file(self, path: pathlib.Path, locale_code: str) -> None:
        pass

    @abstractmethod
    async def save_file(self, path: pathlib.Path | None = None) -> None:
        pass

    @abstractmethod
    async def clean(self) -> None:
        pass

    @abstractmethod
    def is_empty(self) -> bool:
        pass