import pathlib
import typing
from abc import ABC, abstractmethod

import pydantic


class DictProvider(ABC):
    """
    Almost complete abstract implementation of the provider protocol for formats that can be easily
    converted into a dictionary. Requires the implementation of IO methods.
    """

    @classmethod
    async def from_file(cls, path: pathlib.Path, locale_code: str) -> DictProvider:
        """
        Allows you to quickly create a new class instance and immediately load the localisation.
        :param path: Path
        :param locale_code: Localisation code
        :return: New instance
        """

        instance = cls()
        await instance.load_file(path, locale_code)
        return instance

    def __init__(self) -> None:
        self._storage: DataDictModel | None = None

    def __getitem__(self, key: str) -> str | None:
        return self.get(key)

    def __setitem__(self, key: str, value: str) -> str:
        return self.set(key, value)

    def get(self, key: str, default: str | None = None, **kwargs) -> str | None:
        if self._storage is None:
            raise ValueError("The storage is None")

        parts = key.split(".")
        data = self._storage.data

        for part in parts:
            if isinstance(data, dict) and part in data:
                data = data.get(part)
            else:
                return default

        return str(data) if data is not None else default

    def set(self, key: str, value: str) -> str:
        if self._storage is None:
            raise ValueError("The storage is None")

        self._storage.data[key] = value
        return value

    def get_storage(self) -> DataDictModel:
        if self._storage is None:
            raise ValueError("The storage is None")

        return self._storage

    def get_locale_code(self) -> str | None:
        if self._storage is None:
            raise ValueError("The storage is None")

        return self._storage.locale_code

    def get_file_path(self) -> pathlib.Path | None:
        if self._storage is None:
            raise ValueError("The storage is None")

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
    locale_code: str | None  # ISO 15897 (ISO 639-1 + ISO 3166-1 alpha-2)
    path: pathlib.Path | None = None
    version: str = "1.0.0"
