from typing import Dict

import pydantic

from vesna.meta_default_object import MetaDefaultObject

class TranslationModel(pydantic.BaseModel):
    data: Dict[str, str]
    locale_code: str # ISO 15897 (ISO 639-1 + ISO 3166-1 alpha-2)

class Repository(metaclass=MetaDefaultObject):
    def __init__(self) -> None:
        self._storage: Dict[str, TranslationModel] = {}

    async def add_translation(self) -> TranslationModel:
        pass

    async def get_translation(self) -> TranslationModel:
        pass

    async def set_translation(self, data: TranslationModel) -> TranslationModel:
        pass

    def get_text(self, locale_code: str, key: str) -> str | None:
        model: TranslationModel = self._storage.get(locale_code)
        if not model:
            return None

        return model.data.get(key, None)