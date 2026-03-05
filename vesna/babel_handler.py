import babel.dates
import babel.numbers
from babel import Locale

from vesna.meta.meta_default_object import MetaDefaultObject

class BabelHandler(metaclass=MetaDefaultObject):
    def __init__(self):
        self._locale_cache = {}

    def get_locale(self, locale_code: str) -> Locale:
        if locale_code not in self._locale_cache:
            self._locale_cache[locale_code] = Locale.parse(locale_code)
        return self._locale_cache[locale_code]

    def format_date(self, date, locale_code: str, format='medium'):
        return babel.dates.format_date(date, format=format, locale=locale_code)

    def format_currency(self, amount, currency, locale_code: str):
        return babel.numbers.format_currency(amount, currency, locale=locale_code)

    def get_plural_form(self, count, locale_code: str) -> str:
        locale = self.get_locale(locale_code)
        return locale.plural_form(count)