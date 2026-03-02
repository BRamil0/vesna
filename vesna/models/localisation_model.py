import pydantic

class LocalisationModel(pydantic.BaseModel):
    data: dict[str, str]
    locale_code: str # ISO 15897 (ISO 639-1 + ISO 3166-1 alpha-2)
    model_version: str = "1.0.0"