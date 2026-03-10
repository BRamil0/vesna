import datetime
import pathlib

import pytest

from vesna import Locale, Vesna, vesna
from vesna.providers import FluentProvider, GettextProvider, ProviderJSON


@pytest.fixture
def temp_json_locale(tmp_path: pathlib.Path) -> pathlib.Path:
    file_path = tmp_path / "uk.json"
    # Nested structure to match DictProvider dot-notation behavior
    file_path.write_text(
        '{"greeting": "Привіт, {}!", "apples": {"one": "{count} яблуко", "few": "{count} яблука", "many": "{count} яблук", "other": "{count} яблука"}}',  # noqa: E501
        encoding="utf-8",
    )
    return tmp_path


async def test_vesna_fallback(temp_json_locale):
    """Checking fallback logic and error handling."""
    i18n = Vesna()
    i18n.providers = {}
    i18n.default_locale = "uk"

    await i18n.load_file(ProviderJSON(), "uk", temp_json_locale / "uk.json")

    en_path = temp_json_locale / "en.json"
    en_path.write_text('{"other": "Something else"}', encoding="utf-8")
    await i18n.load_file(ProviderJSON(), "en", en_path)

    assert i18n.get_text("greeting", "en") == "Привіт, {}!"
    assert i18n.get_text("not_exist", "en") == "not_exist"

    with pytest.raises(KeyError):
        i18n.get_text("not_exist", "en", is_exception=True)


async def test_locale_babel_formatting(temp_json_locale):
    """Verifying integration with Babel: dates, plural forms, currency."""
    i18n = Vesna()
    i18n.providers = {}
    vesna.providers = {}

    await i18n.load_file(ProviderJSON(), "uk", temp_json_locale / "uk.json")

    locale = Locale("uk", vesna=i18n)

    dt = datetime.date(2026, 3, 10)
    formatted_date = locale.date(dt)
    assert "2026" in formatted_date

    assert locale.currency(100.50, "UAH") == "100,50\xa0₴"
    assert locale.number(1234.56) == "1\xa0234,56"

    # Plural keys: apples.one, apples.few, etc.
    assert locale.plural("apples", 1) == "1 яблуко"
    assert locale.plural("apples", 2) == "2 яблука"
    assert locale.plural("apples", 5) == "5 яблук"


async def test_fluent_provider(tmp_path: pathlib.Path):
    """Checking the Fluent provider and its specific formatting."""
    ftl_path = tmp_path / "uk.ftl"
    ftl_path.write_text(
        "hello-user = Привіт, { $userName }!\nmissing-var = Дані: { $data }", encoding="utf-8"
    )

    provider = FluentProvider(use_isolating=False)
    await provider.load_file(ftl_path, "uk")

    assert provider.get("hello-user", userName="Олексій") == "Привіт, Олексій!"
    assert provider.get("not-exist", default="Дефолт") == "Дефолт"

    with pytest.raises(RuntimeError):
        provider.get("missing-var")


async def test_gettext_provider_po(tmp_path: pathlib.Path):
    """Checking the Gettext (.po) provider."""
    po_content = """
    msgid ""
    msgstr ""
    "Language: uk\\n"

    msgid "hello"
    msgstr "Привіт"
    """
    po_path = tmp_path / "uk.po"
    po_path.write_text(po_content, encoding="utf-8")

    provider = GettextProvider()
    await provider.load_file(po_path, "uk")

    assert provider.get("hello") == "Привіт"
    assert provider.get("missing", default="Fallback") == "Fallback"

    provider.set("hello", "Здоров")
    await provider.save_file()

    provider_new = GettextProvider()
    await provider_new.load_file(po_path, "uk")
    assert provider_new.get("hello") == "Здоров"
