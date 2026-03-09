import io

from ruamel.yaml import YAML
import pathlib

import pydantic
import aiofiles

from vesna.providers.dict_provider import DictProvider, DataDictModel


class ProviderYAML(DictProvider):
    def __init__(self, type: str = "safe"):
        super().__init__()
        self.yaml = YAML(typ=type)

    async def load_file(self, path: pathlib.Path, locale_code: str) -> None:
        await self.clean()

        async with aiofiles.open(path, "r", encoding="utf-8") as f:
            content = await f.read()
            raw_dict = self.yaml.load(content)
            try:
                self._storage = YAMLDataModel.model_validate(raw_dict)
            except pydantic.ValidationError:
                self._storage = YAMLDataModel(
                    data=raw_dict,
                    locale_code=locale_code,
                )

            self._storage.path = path

    async def save_file(self, path: pathlib.Path | None = None) -> None:
        path = pathlib.Path(path) if path else self._storage.path
        if not path:
            raise ValueError(f"Path cannot be None | Path: {path}")

        data_to_save = self._storage.model_dump(exclude={"path"})

        buf = io.BytesIO()

        self.yaml.dump(data_to_save, buf)

        async with aiofiles.open(path, "wb") as f:
            await f.write(buf.getvalue())


class YAMLDataModel(DataDictModel):
    pass
