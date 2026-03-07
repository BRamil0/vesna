import pathlib
import typing
from abc import ABC

import pydantic

from vesna.providers.base import BaseProvider

class Provider(BaseProvider, ABC):
    def __init__(self) -> None:
        self._storage: DataDictModel | None = None

    def __getitem__(self, key: str) -> str:
        return self.get(key)

    def __setitem__(self, key: str, value: str) -> str:
        return self.set(key, value)

    def get(self, key: str, default: str | None = None) -> str:
        parts = key.split('.')
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

    def get_locale_code(self) -> str | None:
        return self._storage.locale_code

    def get_file_path(self) -> pathlib.Path | None:
        return self._storage.path

    async def clean(self) -> None:
        self._storage = None

    def is_empty(self) -> bool:
        return self._storage is None

class DataDictModel(pydantic.BaseModel):
    data: dict[str, typing.Any]
    locale_code: str # ISO 15897 (ISO 639-1 + ISO 3166-1 alpha-2)
    path: pathlib.Path | None = None
    version: str = "1.0.0"