import asyncio

import vesna

async def main():
    await vesna.i18n.load_file(
        vesna.providers.ProviderJSON(),
        "uk",
        "tests/localisation/{locale_code}.json")

    l = vesna.Locale("uk")
    print(l["vesna"])
    print(l("hello", l.get("world")))

if __name__ == "__main__":
    asyncio.run(main())