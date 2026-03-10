import pathlib
import typing
from abc import ABC, abstractmethod

import pydantic


class DictProvider(ABC):
    """
    Almost complete abstract implementation of the provider protocol for formats that can be easily
    converted into a dictionary. Requires the implementation of IO methods.
    """

    def __init__(self) -> None:
        self._storage: DataDictModel | None = None

    def __getitem__(self, key: str) -> str:
        return self.get(key)

    def __setitem__(self, key: str, value: str) -> str:
        return self.set(key, value)

    def get(self, key: str, default: str | None = None, **kwargs) -> str:
        parts = key.split(".")
        data = self._storage.data

        for part in parts:
            if isinstance(data, dict):
                data = data.get(part)
            else:
                return default

        return str(data) if data is not None else default

    def set(self, key: str, value: str) -> str:
        self._storage.data[key] = value
        return value

    def get_storage(self) -> DataDictModel:
        return self._storage

    def get_locale_code(self) -> str | None:
        return self._storage.locale_code

    def get_file_path(self) -> pathlib.Path | None:
        return self._storage.path

    @abstractmethod
    async def load_file(self, path: pathlib.Path, locale_code: str) -> None:
        pass

    @abstractmethod
    async def save_file(self, path: pathlib.Path | None = None) -> None:
        pass

    async def clean(self) -> None:
        self._storage = None

    def is_empty(self) -> bool:
        return self._storage is None


class DataDictModel(pydantic.BaseModel):
    data: dict[str, typing.Any]
    locale_code: str  # ISO 15897 (ISO 639-1 + ISO 3166-1 alpha-2)
    path: pathlib.Path | None = None
    version: str = "1.0.0"
