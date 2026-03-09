import pathlib
from io import StringIO, BytesIO

import pydantic
import aiofiles

from fluent.runtime import FluentBundle, FluentResource

class FluentProvider:
    def __init__(self) -> None:
        self._storage: FluentModel | None = None

    def __getitem__(self, key: str) -> str:
        return self.get(key)

    def __setitem__(self, key: str, value: str) -> str:
        return self.set(key, value)

    def get(self, key: str, default: str | None = None, **kwargs) -> str:
        if not self._storage:
            return default

        bundle = self._storage.data

        if not bundle.has_message(key):
            return default

        message = bundle.get_message(key)
        if message.value is None:
            return default

        formatted_string, errors = bundle.format_pattern(message.value, kwargs)
        if errors:
            RuntimeError(f"{errors}")

        return formatted_string

    def set(self, key: str, value: str) -> str:
        raise NotImplementedError("Fluent provider currently does not support runtime editing.")

    def get_storage(self) -> FluentModel:
        return self._storage

    def get_locale_code(self) -> str | None:
        return self._storage.locale_code if self._storage else None

    def get_file_path(self) -> pathlib.Path | None:
        return self._storage.path if self._storage else None

    async def load_file(self, path: pathlib.Path, locale_code: str) -> None:
        await self.clean()

        async with aiofiles.open(path, "r", encoding="utf-8") as f:
            content = await f.read()

            resource = FluentResource(content)

            bundle = FluentBundle([locale_code])
            bundle.add_resource(resource)

            self._storage = FluentModel(
                data=bundle,
                path=path
            )

    async def save_file(self, path: pathlib.Path | None = None) -> None:
        raise NotImplementedError("Fluent provider currently does not support runtime saving.")

    async def clean(self) -> None:
        self._storage = None

    def is_empty(self) -> bool:
        return self._storage is None

class FluentModel(pydantic.BaseModel):
    model_config = pydantic.ConfigDict(arbitrary_types_allowed=True)

    data: FluentBundle
    path: pathlib.Path | None = None

    version: str = "1.0.0"

    @property
    def locale_code(self) -> str | None:
        if self.data and hasattr(self.data, 'locales') and self.data.locales:
            return self.data.locales[0]
        return None