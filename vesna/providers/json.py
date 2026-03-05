import json
import pathlib
import typing

import pydantic
import aiofiles

from vesna.providers.base import BaseProvider

class ProviderJSON(BaseProvider):
    def __init__(self) -> None:
        self._storage: JSONDataModel | None = None

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

    async def load_file(self, path: pathlib.Path, locale_code: str) -> None:
        await self.clean()

        async with aiofiles.open(path, "r", encoding="utf-8") as f:
            content = await f.read()
            try:
                self._storage = JSONDataModel.model_validate_json(content)
            except pydantic.ValidationError:
                raw_dict = json.loads(content)

                self._storage = JSONDataModel(
                    data=raw_dict,
                    locale_code=locale_code,
                )

            self._storage.path = path

    async def save_file(self, path: pathlib.Path | None = None) -> None:
        path = pathlib.Path(path) if path else self._storage.path
        if not path:
            raise ValueError(f"Path cannot be None | Path: {path}")

        async with aiofiles.open(path, "w", encoding="utf-8") as f:
            await f.write(self._storage.model_dump_json())

    async def clean(self) -> None:
        self._storage = None

    def is_empty(self) -> bool:
        return self._storage is None

class JSONDataModel(pydantic.BaseModel):
    data: dict[str, typing.Any]
    locale_code: str # ISO 15897 (ISO 639-1 + ISO 3166-1 alpha-2)
    path: pathlib.Path | None = None
    version: str = "1.0.0"