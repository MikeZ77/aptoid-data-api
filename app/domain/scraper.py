from typing import cast

import falcon
from aiohttp import ClientConnectionError, ClientResponseError, ClientSession
from lxml import html

from app.utils.exceptions import HtmlParsingError


class ContentScraper:
    def __init__(self, xpath: dict[str, str], session: ClientSession):
        self.session = session
        self.xpath = xpath
        self.output: dict[str, str] = {}

    async def _fetch_content(self, url: str) -> str:
        try:
            async with self.session.get(url) as response:
                response.raise_for_status()
                return await response.text()
        except ClientResponseError:
            raise falcon.HTTPError(
                falcon.HTTP_400, f"App for {url} is not found. Please check the URL"
            )
        except ClientConnectionError:
            raise falcon.HTTPError(
                falcon.HTTP_500, f"Error connecting to {url}. Please try again later"
            )

    def _parse_data(self, path: str, html_ele: html.HtmlElement) -> list[str]:
        return cast(list[str], html_ele.xpath(path))

    async def __call__(self, url: str) -> dict[str, str]:
        html_str = await self._fetch_content(url)
        html_ele = html.fromstring(html_str)

        for name, path in self.xpath.items():
            self.output[name] = "\n\n".join(self._parse_data(path, html_ele))

        if any(not value for value in self.output.values()):
            raise HtmlParsingError(self.output)

        return self.output
