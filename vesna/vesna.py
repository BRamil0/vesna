import pathlib

import babel

from vesna.meta.meta_default_object import MetaDefaultObject
from vesna.parser import Parser
from vesna.repository import Repository, LocalisationModel

class Vesna(metaclass=MetaDefaultObject):
    @MetaDefaultObject.meta_inject(auto_creation=True)
    def __init__(self, parser: Parser, repository: Repository, is_exception: bool = False) -> None:
        self.parser: Parser = parser
        self.repository: Repository = repository
        self.default_locale: str | None = None
        self.is_exception: bool = is_exception

    async def load_translation(self, default_path: pathlib.Path | None = None,
                               default_file_name: str = "{locale_code}",
                               *args: str, **kwargs: str) -> bool:
        """
        :param default_path: Path for dir
        :param default_file_name: File name, write {locale_code} for the code
        :param args: Locale code
        :param kwargs: Locale code + File name, write {locale_code} for the code
        :return: Returns True if everything is fine. Returns False if the file is not found. Returns an exception if they occurred.
        """

        base_path = default_path or self.parser.path
        if not base_path and args:
            raise KeyError("Base path for positional arguments (*args) not set")

        if default_path:
            await self.parser.set_path(default_path)

        if not default_file_name:
            raise TypeError("The path must be an object of pathlib.Path or String.")

        loaded_models: list[LocalisationModel] = []
        if isinstance(base_path, str):
            base_path = pathlib.Path(base_path)
        elif not isinstance(base_path, pathlib.Path) and not isinstance(base_path, pathlib.Path):
            raise KeyError("Base path for positional arguments (*args) not set")
        try:
            for code in args:
                file_name = default_file_name.format(locale_code=code)
                model = await self.parser.parse(file_name, base_path)
                loaded_models.append(model)

            for code, value in kwargs.items():
                if "{locale_code}" in value:
                    full_path = pathlib.Path(value.format(locale_code=code))
                    model = await self.parser.parse(full_path.name, full_path.parent)
                else:
                    file_name = default_file_name.format(locale_code=code)
                    model = await self.parser.parse(file_name, pathlib.Path(value))

                loaded_models.append(model)

            for model in loaded_models:
                await self.repository.update(model.locale_code, model)
        except FileNotFoundError:
            return False

        return True

    def get_text(self, key: str, locale_code: str) -> str:
        value: str = self.repository.get_text(key, locale_code)
        if value is None:
            if self.default_locale and locale_code != self.default_locale:
                return self.get_text(key, self.default_locale)
            elif self.is_exception:
                raise KeyError("Key not found")

        return value or key

    async def aget_text(self, key: str, locale_code: str,
                        lazy_loading: bool = False,
                        lazy_path: pathlib.Path | None = None,
                        lazy_file_name: str = "{locale_code}") -> str:
        value: str = self.repository.get_text(key, locale_code)
        if value is None:
            if lazy_loading and await self.load_translation(lazy_path, lazy_file_name, locale_code):
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
