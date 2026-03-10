## Vesna

__[Українська](README.uk.md)__

#### Description
A lightweight library specialized in convenient localization (i18n).

### Installation

Via `uv` (**recommended**):
- `uv pip install vesna` — Minimal
- `uv pip install vesna[all]` — Full

Via `pip`:
- `python -m pip install vesna` — Minimal
- `python -m pip install vesna[all]` — Full

### Quick Start

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

### Features
- Support for multiple localization formats
- Convenient syntax with `[]` and `()` support
- `Babel` integration

### Usage

#### Providers
- `FluentProvider`: Fluent format (requires `fluent.runtime`).
- `GettextProvider`: GNU Gettext format (requires `Babel`).
- `ProviderJSON`: JSON format (uses `pydantic_core`, requires `pydantic`).
- `ProviderJSON5`: JSON5 format (requires `json5` or `pyjson5`).
- `ProviderHJSON`: HJSON format (requires `hjson`).
- `ProviderTOML`: TOML format (requires `rtoml`).
- `ProviderYAML`: YAML format (requires `ruamel.yaml`).

#### Creating a custom `Vesna` instance
```python
import vesna
v = vesna.Vesna()
# Set as the global default object
v.default_object = v
```

### License
This project is licensed under the **MIT** License. See the [LICENSE](LICENSE) file for details.