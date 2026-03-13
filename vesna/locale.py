import datetime

try:
    import babel

    from vesna.babel_handler import BabelHandler

    SUPPORT_BABEL = True
except ImportError:
    babel = None
    BabelHandler = None

    SUPPORT_BABEL = False

from vesna.meta.meta_cache import MetaCache
from vesna.vesna import Vesna


class Locale(metaclass=MetaCache):
    """
    Provides a basic API for working with a single localisation.
    """

    @Vesna.meta_inject(auto_creation=True)
    def __init__(self, locale_code: str, vesna: Vesna, babel_handler: BabelHandler) -> None:
        self.locale_code: str = locale_code
        self.vesna: Vesna = vesna
        self.babel_handler: BabelHandler = babel_handler

    def __getitem__(self, key: str) -> str:
        return self.vesna.get_text(key, self.locale_code)

    def __call__(self, key: str, *args, **kwargs) -> str:
        return self.format(key, *args, **kwargs)

    def format(self, key: str, *args, **kwargs) -> str:
        text = self.vesna.get_text(key, self.locale_code)
        return text.format(*args, **kwargs) if (args or kwargs) else text

    def get(self, key: str, default: str = None) -> str:
        return self.vesna.get_text(key, self.locale_code, default)

    if SUPPORT_BABEL:

        @property
        def babel(self) -> babel.Locale:
            return self.babel_handler.get_locale(self.locale_code)

        def date(
            self, value: datetime.date | datetime.datetime | datetime.time, format: str = "medium"
        ) -> str:
            return self.babel_handler.format_date(value, self.locale_code, format)

        def plural(self, key: str, count: int, **kwargs) -> str:
            plural_form = self.babel_handler.get_plural_form(count, self.locale_code)

            full_key = f"{key}.{plural_form}"
            text = self.get(full_key)

            if text == full_key:
                text = self.get(key)

            return text.format(count=count, **kwargs)

        def currency(self, amount: float | int, currency_code: str = "USD") -> str:
            return self.babel_handler.format_currency(amount, currency_code, self.locale_code)

        def number(self, value: float | int) -> str:
            return self.babel_handler.format_decimal(value, self.locale_code)
