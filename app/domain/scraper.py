from aiohttp import ClientSession
from lxml import html

from app.utils.exceptions import HtmlParsingError


class ContentScraper:
    def __init__(self, xpath: dict[str, str], session: ClientSession):
        self.session = session
        self.xpath = xpath
        self.output: dict[str, str] = {}

    async def _fetch_content(self, url: str) -> str:
        async with self.session.get(url) as response:
            return await response.text()

    def _parse_data(self, path: str, html_ele: html.HtmlElement) -> list[str]:
        value = html_ele.xpath(path)
        return value if value else []

    async def __call__(self, url: str) -> dict[str, str]:
        html_str = await self._fetch_content(url)
        html_ele = html.fromstring(html_str)

        for name, path in self.xpath.items():
            self.output[name] = "\n\n".join(self._parse_data(path, html_ele))

        if any(value is None for value in self.output.values()):
            raise HtmlParsingError(self.output)

        return self.output
