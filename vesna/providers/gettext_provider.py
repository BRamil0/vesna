import pathlib
from io import StringIO, BytesIO

import pydantic
import aiofiles

from babel.messages.catalog import Catalog
from babel.messages.pofile import read_po, write_po
from babel.messages.mofile import read_mo, write_mo

class GettextProvider:
    def __init__(self) -> None:
        self._storage: GettextModel | None = None

    def __getitem__(self, key: str) -> str:
        return self.get(key)

    def __setitem__(self, key: str, value: str) -> str:
        return self.set(key, value)

    def get(self, key: str, default: str | None = None) -> str:
        if not self._storage:
            return default

        message = self._storage.data.get(key)

        if message and message.string:
            if isinstance(message.string, str):
                return message.string
            elif isinstance(message.string, tuple):
                return message.string[0]

        return default

    def set(self, key: str, value: str) -> str:
        if not self._storage:
            raise RuntimeError("Storage is empty")

        if key in self._storage.data:
            self._storage.data[key].string = value
        else:
            self._storage.data.add(key, string=value)

        return value

    def get_storage(self) -> GettextModel:
        return self._storage

    def get_locale_code(self) -> str | None:
        if self._storage and self._storage.data.locale:
            return str(self._storage.data.locale)
        return None

    def get_file_path(self) -> pathlib.Path | None:
        return self._storage.path if self._storage else None

    async def load_file(self, path: pathlib.Path, locale_code: str) -> None:
        await self.clean()

        if path.suffix == '.mo':
            # Читаємо бінарний MO файл
            async with aiofiles.open(path, "rb") as f:
                content = await f.read()

                buf = BytesIO(content)
                catalog = read_mo(buf)
                catalog.locale = locale_code
        else:
            async with aiofiles.open(path, "r", encoding="utf-8") as f:
                content = await f.read()

                buf = StringIO(content)
                catalog = read_po(buf, locale=locale_code)

        self._storage = GettextModel(
            data=catalog,
            path=path
        )

    async def save_file(self, path: pathlib.Path | None = None) -> None:
        target_path = path or (self._storage.path if self._storage else None)
        if not target_path or not self._storage:
            raise ValueError("Path or storage is empty")

        buf = BytesIO()
        write_po(buf, self._storage.data)

        async with aiofiles.open(target_path, "wb") as f:
            await f.write(buf.getvalue())

    async def compile_mo(self, path: pathlib.Path | None = None) -> None:
        if not self._storage:
            raise RuntimeError("Storage is empty, nothing to compile")

        target_path = path
        if not target_path:
            if self._storage.path:
                target_path = self._storage.path.with_suffix('.mo')
            else:
                raise ValueError("Path is empty")

        buf = BytesIO()
        write_mo(buf, self._storage.data)

        async with aiofiles.open(target_path, "wb") as f:
            await f.write(buf.getvalue())

    async def clean(self) -> None:
        self._storage = None

    def is_empty(self) -> bool:
        return self._storage is None

class GettextModel(pydantic.BaseModel):
    model_config = pydantic.ConfigDict(arbitrary_types_allowed=True)

    data: Catalog
    path: pathlib.Path | None = None

    version: str = "1.0.0"

    @property
    def locale_code(self) -> str | None:
        return str(self.data.locale) if self.data.locale else None