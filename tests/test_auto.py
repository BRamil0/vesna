import pytest

from vesna import providers

@pytest.mark.parametrize("provider_cls, filename", [
    (providers.ProviderJSON, "uk.json"),
    (providers.ProviderJSON5, "uk.json5"),
    (providers.ProviderHJSON, "uk.hjson"),
    (providers.ProviderYAML, "uk.yaml"),
    (providers.ProviderTOML, "uk.toml"),
])
async def test_provider_load_save(provider_cls, filename, tmp_path):
    file_path = tmp_path / filename

    provider = provider_cls()

    await provider.load_file("tests/localisation/" + filename, "uk")
    await provider.save_file(file_path)


    await provider.load_file(file_path, "uk")
    assert provider.get("hello") == "Привіт {}"

    provider.set("hello", "Здоров {}")
    await provider.save_file()

    await provider.load_file(file_path, "uk")
    assert provider.get("hello") == "Здоров {}"