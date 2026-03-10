## Весна (Vesna)

__[English](README.md)__

#### Опис
Невелика бібліотека спеціалізована на зручній локалізації

### Встановлення

Через `uv` (**рекомендовано**):
- `uv pip install vesna` — Мінімальна
- `uv pip install vesna[all]` — Повна

Через `pip`:
- `python -m pip install vesna` — Мінімальна
- `python -m pip install vesna[all]` — Повна

### Швидкий старт

```python
import vesna

async def main():
    await vesna.i18n.load_file(
        vesna.providers.ProviderJSON(), "uk", "tests/localisation/{locale_code}.json"
    )

    l = vesna.Locale("uk")
    print(l["vesna"])
    print(l("hello", l.get("world")))
```

### Особливості
- Підтримка декількох форматів
- Підтримка `[]` та `()`
- Підтримка `Babel`

###  Використання

#### Провайдери
- `FluentProvider`: Формат Fluent (потребує `fluent.runtime`).
- `GettextProvider`: Формат GHU Gettext (потребує `Babel`).
- `ProviderJSON`: Формат JSON (потребує `pydantic`, використовує `pydantic_core`).
- `ProviderJSON5`: Формат JSON5 (потребує `json5` або `pyjson5`).
- `ProviderHJSON`: Формат HJSON (потребує `hjson`).
- `ProviderYAML`: Формат YAML (потребує `ruamel.yaml`).
- `ProviderTOML`: Формат TOML (потребує `rtoml`).

#### Створення окремого класу "`Vesna`"
```python
import vesna
v = vesna.Vesna()
# Додаємо як глобальний об'єкт
v.default_object = v
```

### Ліцензія
Цей проєкт ліцензовано за ліцензією **MIT**. Детальніше дивіться у файлі [LICENSE](LICENSE).