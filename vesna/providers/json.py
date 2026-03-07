import pathlib

import pydantic
from pydantic_core import from_json
import aiofiles

from vesna.providers.provider import Provider, DataDictModel

class ProviderJSON(Provider):
    async def load_file(self, path: pathlib.Path, locale_code: str) -> None:
        await self.clean()

        async with aiofiles.open(path, "r", encoding="utf-8") as f:
            content = await f.read()

            try:
                self._storage = JSONDataModel.model_validate_json(content)
            except pydantic.ValidationError:
                raw_dict = from_json(content)

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

class JSONDataModel(DataDictModel):
    pass