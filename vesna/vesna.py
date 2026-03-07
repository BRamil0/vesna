import pathlib

from vesna.meta.meta_default_object import MetaDefaultObject
from vesna.providers import ProviderProtocol

class Vesna(metaclass=MetaDefaultObject):
    @MetaDefaultObject.meta_inject(auto_creation=True)
    def __init__(self, default_locale: str | None = None, default_path: pathlib.Path | str | None = None) -> None:

        self.providers: dict[str, ProviderProtocol] = {}
        self.default_locale: str | None = default_locale
        self.default_path: pathlib.Path | str | None = default_path

    def _path_handler(self, path: pathlib.Path | str | None, locale_code: str) -> pathlib.Path:
        if isinstance(path, str):
            if "{locale_code}" in path:
                path = path.format(locale_code=locale_code)

            path = pathlib.Path(path)

        if not path.is_file():
            raise FileNotFoundError(path)

        return path

    async def load_file(self, provider: ProviderProtocol | None = None,
                        locale_code: str | None = None,
                        path: pathlib.Path | str | None = None) -> None:
        locale_code = locale_code or self.default_locale
        if not locale_code:
            raise RuntimeError("Locale code is None")

        if provider:
            self.providers[locale_code] = provider

        provider = provider or self.providers.get(locale_code, None)
        if not provider:
            raise RuntimeError("Provider is None")

        if not provider.is_empty():
            raise RuntimeError("Provider is not empty")

        path = path or self.default_path
        if not path:
            raise RuntimeError("Path is None")
        path: pathlib.Path = self._path_handler(path, locale_code)

        await provider.load_file(path, locale_code)

    async def save_file(self, locale_code: str | None = None, path: pathlib.Path | str | None = None) -> None:
        locale_code = locale_code or self.default_locale
        if not locale_code:
            raise RuntimeError("Locale code is None")

        path = path or self.default_path
        path: pathlib.Path = self._path_handler(path, locale_code)

        await self.providers[locale_code].save_file(path)

    def get_text(self, key: str, locale_code: str, is_exception: bool = False) -> str:
        try:
            provider = self.providers.get(locale_code)
            if not provider:
                raise KeyError(f"Locale '{locale_code}' not loaded")
            value = provider.get(key, default=None)

            if value is None:
                raise KeyError(f"Key '{key}' missing")

            return value
        except KeyError as e:
            if self.default_locale and locale_code != self.default_locale:
                return self.get_text(key, self.default_locale, is_exception)

            if is_exception:
                raise KeyError(f"Key '{key}' not found in '{locale_code}'") from e
            return key

    def set_text(self, key: str, value: str, locale_code: str, is_exception: bool = False) -> str:
        provider = self.providers.get(locale_code)
        if not provider:
            if is_exception:
                raise KeyError(f"Locale '{locale_code}' not loaded")
            return key
        return provider.set(key, value)

vesna: Vesna = Vesna()

I18n: Vesna = Vesna
i18n: I18n = vesna
Internationalization: Vesna = Vesna
internationalization: Internationalization = vesna
