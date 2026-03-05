import datetime
import pathlib

import babel

from vesna.babel_handler import BabelHandler
from vesna.vesna import Vesna

from vesna.meta.meta_cache import MetaCache

class Locale(metaclass=MetaCache):
    @Vesna.meta_inject(auto_creation=True)
    def __init__(self, locale_code: str, vesna: Vesna, babel_handler: BabelHandler) -> None:
        self.locale_code: str = locale_code
        self.vesna: Vesna = vesna
        self.babel_handler: BabelHandler = babel_handler

    def __getitem__(self, key: str) -> str:
        return self.vesna.get_text(key, self.locale_code)

    def get(self, key: str) -> str:
        return self.vesna.get_text(key, self.locale_code)

    async def aget(self, key: str, lazy_loading: bool = False,
                        lazy_path: pathlib.Path | None = None,
                        lazy_file_name: str = "{locale_code}") -> str:
        return await self.vesna.aget_text(key, self.locale_code, lazy_loading, lazy_path, lazy_file_name)

    @property
    def babel(self) -> babel.Locale:
        return self.babel_handler.get_locale(self.locale_code)

    def date(self, value: datetime.datetime, format: str = 'medium') -> str:
        return self.babel_handler.format_date(value, self.locale_code, format)

    def plural(self, key: str, count: int, **kwargs) -> str:
        plural_form = self.babel_handler.get_plural_form(count, self.locale_code)

        full_key = f"{key}.{plural_form}"
        text = self.get(full_key)

        if text == full_key:
            text = self.get(key)

        return text.format(count=count, **kwargs)