import asyncio

import vesna.locale

async def main():
    l = vesna.locale.Locale("en")
    print(l["test"])

if __name__ == "__main__":
    asyncio.run (main())