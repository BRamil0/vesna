from vesna.meta.meta_default_object import MetaDefaultObject
from vesna.models.localisation_model import LocalisationModel


class Repository(metaclass=MetaDefaultObject):
    def __init__(self) -> None:
        self._storage: dict[str, LocalisationModel] = {}

    def __getitem__(self, model: str) -> str:
        return self._storage.__getitem__(model)

    async def get(self, locale_code: str) -> LocalisationModel:
        return self._storage.get(locale_code)

    async def update(self, locale_code: str, model: LocalisationModel) -> None:
        self._storage.update({locale_code: model})

    async def pop(self, locale_code: str) -> None:
        self._storage.pop(locale_code)

    async def clear(self) -> None:
        self._storage.clear()

    def get_text(self, key: str, locale_code: str) -> str | None:
        model: LocalisationModel = self._storage.get(locale_code)
        if not model:
            return None

        return model.data.get(key, None)