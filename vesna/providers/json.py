import json
import pathlib
import typing

import aiofiles

from vesna.providers.base import BaseProvider

class ProviderJSON(BaseProvider):
    def __init__(self) -> None:
        self._storage: dict[str, typing.Any] = {}

    def __getitem__(self, key: str) -> str:
        return self.get(key)

    def __setitem__(self, key: str, value: str) -> str:
        return self.set(key, value)

    def get(self, key: str, default: str | None = None) -> str:
        if default:
            return self._storage.get(key, default)
        return self._storage.get(key)

    def set(self, key: str, value: str) -> str:
        self._storage[key] = value
        return value

    async def load_file(self, path: pathlib.Path) -> None:
        async with aiofiles.open(path, "r", encoding="utf-8") as f:
            content = await f.read()
            self._storage = json.loads(content)

    async def save_file(self, path: pathlib.Path) -> None:
        async with aiofiles.open(path, "w", encoding="utf-8") as f:
            await f.write(json.dumps(self._storage))

    async def clean(self) -> None:
        self._storage.clear()