import pathlib

from vesna.babel_handler import BabelHandler
from vesna.meta_default_object import MetaDefaultObject
from vesna.parser import Parser
from vesna.repository import Repository

class Vesna(metaclass=MetaDefaultObject):
    def __init__(self, parser: Parser | None = None, repository: Repository | None = None, is_exception: bool = False) -> None:
        self.parser: Parser = parser or Parser()
        self.repository: Repository = repository or Repository()
        self.babel: BabelHandler = BabelHandler()
        self.default_locale: str | None = None
        self.is_exception: bool = is_exception

    async def load_translation(self, default_path: pathlib.Path, *args, **kwargs) -> Vesna:
        pass

    def get_text(self, key: str, locale_code: str) -> str:
        value: str = self.repository.get_text(key, locale_code)
        if value is None:
            if self.default_locale and locale_code != self.default_locale:
                return self.get_text(key, self.default_locale)
            elif self.is_exception:
                raise KeyError("Key not found")

        return value or key

    async def aget_text(self, key: str, locale_code: str, lazy_loading: bool = False) -> str:
        value: str = self.repository.get_text(key, locale_code)
        if value is None:
            if lazy_loading and await self.parser.parse(locale_code):
                return await self.aget_text(key, locale_code)
            elif self.default_locale and locale_code != self.default_locale:
                return await self.aget_text(key, self.default_locale)
            elif self.is_exception:
                raise KeyError("Key not found")

        return value or key


vesna: Vesna = Vesna()

I18n: Vesna = Vesna
i18n: I18n = vesna
Internationalization: Vesna = Vesna
internationalization: Internationalization = vesna
