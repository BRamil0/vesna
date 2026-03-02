import pathlib
import json

import pydantic
import aiofiles

from vesna.meta.meta_default_object import MetaDefaultObject
from vesna.models.localisation_model import LocalisationModel


class Parser(metaclass=MetaDefaultObject):
    def __init__(self, path: pathlib.Path | None = None) -> None:
        self.path: pathlib.Path | None = path or None

    async def set_path(self, path: pathlib.Path) -> None:
        self.path: pathlib.Path | None = path

    async def parse(self, file_name: str, path: pathlib.Path | None = None) -> LocalisationModel:
        path: pathlib.Path = path or self.path

        if not isinstance(file_name, str):
            raise TypeError("The file_name must be an object of str (String) and not be None.")

        if not isinstance(path, pathlib.Path):
            raise TypeError("The path must be an object of pathlib.Path and not be None.")

        clean_file_name = file_name.lstrip("/")
        full_path = path / clean_file_name

        async with aiofiles.open(full_path, "r", encoding="utf-8") as f:
            content = await f.read()
            try:
                return LocalisationModel.model_validate_json(content)
            except pydantic.ValidationError as e:
                raw_dict = json.loads(content)

                locale_code = file_name.split('.')[0]

                return LocalisationModel(
                    data=raw_dict,
                    locale_code=locale_code
                )