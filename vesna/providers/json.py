import json
import pathlib
import typing

import aiofiles

from vesna.providers.base import BaseProvider

class ProviderJSON(BaseProvider):
    def __init__(self) -> None:
        self._storage: dict[str, typing.Any] = {}
        self._locale_code: str | None = None
        self._path: pathlib.Path | None = None

    def __getitem__(self, key: str) -> str:
        return self.get(key)

    def __setitem__(self, key: str, value: str) -> str:
        return self.set(key, value)

    def get(self, key: str, default: str | None = None) -> str:
        parts = key.split('.')
        data = self._storage

        for part in parts:
            if isinstance(data, dict):
                data = data.get(part)
            else:
                return default

        return str(data) if data is not None else default

    def set(self, key: str, value: str) -> str:
        self._storage[key] = value
        return value

    def get_locale_code(self) -> str | None:
        return self._locale_code

    def get_file_path(self) -> pathlib.Path | None:
        return self._path

    async def load_file(self, path: pathlib.Path, locale_code: str) -> None:
        await self.clean()

        self._locale_code = locale_code
        self._path = path

        async with aiofiles.open(path, "r", encoding="utf-8") as f:
            content = await f.read()
            self._storage = json.loads(content)

    async def save_file(self, path: pathlib.Path) -> None:
        async with aiofiles.open(path, "w", encoding="utf-8") as f:
            await f.write(json.dumps(self._storage))

    async def clean(self) -> None:
        self._storage.clear()
        self._locale_code = None
        self._path = None

    def is_empty(self) -> bool:
        return len(self._storage) == 0