import asyncio

import vesna

async def main():
    await vesna.i18n.load_file(
        vesna.ProviderJSON(),
        "uk",
        "tests/localisation/{locale_code}.json")

    l = vesna.Locale("uk")
    print(l["hello"])

if __name__ == "__main__":
    asyncio.run(main())