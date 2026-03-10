import pathlib

import aiofiles
import hjson
import pydantic

from vesna.providers.dict_provider import DataDictModel, DictProvider


class ProviderHJSON(DictProvider):
    """
    Implementation of IO methods for DictProvider to support the HJSON format.
    """

    async def load_file(self, path: pathlib.Path, locale_code: str) -> None:
        await self.clean()

        async with aiofiles.open(path, "r", encoding="utf-8") as f:
            content = await f.read()
            raw_dict = hjson.loads(content)
            try:
                self._storage = HJSONDataModel.model_validate(raw_dict)
            except pydantic.ValidationError:
                self._storage = HJSONDataModel(
                    data=raw_dict,
                    locale_code=locale_code,
                )

            self._storage.path = path

    async def save_file(self, path: pathlib.Path | None = None) -> None:
        path = pathlib.Path(path) if path else self._storage.path
        if not path:
            raise ValueError(f"Path cannot be None | Path: {path}")

        data_to_save = self._storage.model_dump(exclude={"path"})

        async with aiofiles.open(path, "wb") as f:
            hjson_string = hjson.dumps(data_to_save)
            await f.write(hjson_string.encode("utf-8"))


class HJSONDataModel(DataDictModel):
    pass
