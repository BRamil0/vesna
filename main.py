import asyncio

import vesna

async def main():
    vesna.i18n.is_exception = True
    print(await vesna.i18n.load_translation(
        "tests/localisation/",
        "{locale_code}.json",
        "uk"))

    l = vesna.Locale("uk")
    print(l["hello"])

if __name__ == "__main__":
    asyncio.run(main())