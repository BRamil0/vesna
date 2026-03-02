import pathlib

from vesna.vesna import Vesna

from vesna.meta.meta_cache import MetaCache

class Locale(metaclass=MetaCache):
    def __init__(self, locale_code: str, vesna: Vesna | None = None) -> None:
        self.locale_code: str = locale_code
        self.vesna: Vesna = vesna or Vesna.default_object or Vesna()

    def __getitem__(self, key: str) -> str:
        return self.vesna.get_text(key, self.locale_code)

    def get(self, key: str) -> str:
        return self.vesna.get_text(key, self.locale_code)

    async def aget(self, key: str, lazy_loading: bool = False,
                        lazy_path: pathlib.Path | None = None,
                        lazy_file_name: str = "{locale_code}") -> str:
        return await self.vesna.aget_text(key, self.locale_code, lazy_loading, lazy_path, lazy_file_name)
