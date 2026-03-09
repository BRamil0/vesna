try:
    import json5
    pyjson5 = None

    json5lib = json5
except ImportError:
    import pyjson5
    json5 = None

    json5lib = pyjson5


import pathlib

import pydantic
import aiofiles

from vesna.providers.dict_provider import DictProvider, DataDictModel

class ProviderJSON5(DictProvider):
    async def load_file(self, path: pathlib.Path, locale_code: str) -> None:
        await self.clean()

        async with aiofiles.open(path, "r", encoding="utf-8") as f:
            content = await f.read()
            raw_dict = json5lib.loads(content)
            try:
                self._storage = JSON5DataModel.model_validate(raw_dict)
            except pydantic.ValidationError:
                self._storage = JSON5DataModel(
                    data=raw_dict,
                    locale_code=locale_code,
                )

            self._storage.path = path

    async def save_file(self, path: pathlib.Path | None = None) -> None:
        path = pathlib.Path(path) if path else self._storage.path
        if not path:
            raise ValueError(f"Path cannot be None | Path: {path}")

        data_to_save = self._storage.model_dump(exclude={'path'})

        async with aiofiles.open(path, "wb") as f:
            toml_string = json5lib.dumps(data_to_save)
            await f.write(toml_string.encode("utf-8"))

class JSON5DataModel(DataDictModel):
    pass