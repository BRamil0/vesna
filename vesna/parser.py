from vesna.repository import Repository


class Parser:
    def __init__(self, repository: Repository | None = None) -> None:
        self.repository: Repository = repository or Repository.default_object

    async def parse(self, locale_code: str) -> bool:
        return False