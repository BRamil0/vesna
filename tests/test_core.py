import pytest

import vesna


@pytest.fixture(autouse=True)
async def setup_i18n():
    try:
        await vesna.i18n.load_file(
            vesna.providers.ProviderJSON(), "uk", "tests/localisation/{locale_code}.json"
        )
    except (RuntimeError, KeyError, FileNotFoundError):
        pytest.fail("Failed to load translation file")


@pytest.fixture
def locale():
    return vesna.Locale("uk")


async def test_load():
    provider = vesna.providers.ProviderJSON()
    locale_code = "en"
    path = "tests/localisation/{locale_code}.json"
    i18n = vesna.Vesna()

    with pytest.raises(RuntimeError):
        await i18n.load_file(None, locale_code, path)

    with pytest.raises(RuntimeError):
        await i18n.load_file(provider, None, path)

    with pytest.raises(RuntimeError):
        await i18n.load_file(provider, locale_code, None)

    await i18n.load_file(provider, locale_code, path)


async def test_save():
    with pytest.raises(AttributeError):
        await vesna.i18n.save_file("en")

    with pytest.raises(RuntimeError):
        await vesna.i18n.save_file(None)


def test_get(locale):
    assert locale.get("hello") == "Привіт {}"


def test_key(locale):
    assert locale["hello"] == "Привіт {}"
