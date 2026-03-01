from vesna.vesna import Vesna

from vesna.meta_cache import MetaCache

class Locale(metaclass=MetaCache):
    def __init__(self, locale_code: str, vesna: Vesna | None = None) -> None:
        self.locale_code: str = locale_code
        self.vesna: Vesna = vesna or Vesna.default_object

    def __getitem__(self, key: str) -> None:
        return self.vesna.get_text(key, self.locale_code)

    def get(self, key: str) -> None:
        return self.vesna.get_text(key, self.locale_code)

    async def aget(self, key: str, lazy_loading: bool = False) -> None:
        return await self.vesna.aget_text(key, self.locale_code, lazy_loading)
