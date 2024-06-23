from __future__ import annotations

import pytest

from app.config.models import Sites
from app.domain.scraper import ContentScraper
from app.utils.exceptions import HtmlParsingError


class MockRequestContextManager:
    def __init__(self, response: str):
        self.response = response

    async def __aenter__(self) -> MockRequestContextManager:
        return self

    async def __aexit__(self, *args: tuple[Exception, Exception, Exception]) -> None:
        pass

    async def text(self) -> str:
        return self.response

    def raise_for_status(self) -> None:
        pass


class MockClientSession:
    def __init__(self, response: str):
        self.response = response

    def get(self, _: str) -> MockRequestContextManager:
        return MockRequestContextManager(self.response)


async def scrape_aptoid_content(
    page_data: dict[str, str], scrape_configs: Sites, value: str
) -> str:
    html = page_data["aptoid_dragon_city"]
    aptoid_xpath = scrape_configs.aptoid.xpath.model_dump(by_alias=True)
    xpath = {xpath: query for xpath, query in aptoid_xpath.items() if xpath == value}
    # TODO: Would need create a protocol or ABC for ClientSession since ContentScraper
    # expected a ClientSession not MockClientSession
    return (await ContentScraper(xpath, MockClientSession(html))(""))[value]  # type: ignore


@pytest.mark.asyncio
async def test_unit_content_scraper_finds_app_name(
    page_data: dict[str, str], scrape_configs: Sites
) -> None:
    output = await scrape_aptoid_content(page_data, scrape_configs, "appName")
    assert output == "Dragon City"


@pytest.mark.asyncio
async def test_unit_content_scraper_finds_app_version(
    page_data: dict[str, str], scrape_configs: Sites
) -> None:
    output = await scrape_aptoid_content(page_data, scrape_configs, "appVersion")
    assert output == "24.6.0"


@pytest.mark.asyncio
async def test_unit_content_scraper_finds_app_downloads(
    page_data: dict[str, str], scrape_configs: Sites
) -> None:
    output = await scrape_aptoid_content(page_data, scrape_configs, "appDownloads")
    assert output == "4M+"


@pytest.mark.asyncio
async def test_unit_content_scraper_finds_app_description(
    page_data: dict[str, str], scrape_configs: Sites
) -> None:
    output = await scrape_aptoid_content(page_data, scrape_configs, "appDescription")
    assert (
        output
        == "Ready to master one of your favorite dragon games? Download \
Dragon City Mobile to fight and feed adorable fire-breathing dragons in this epic \
PvP adventure!\n\nBuild floating islands in Dragon City Mobile, fill it with farms, \
habitats, buildings…and tons of dragons! Train them up, feed and evolve them into \
beasts of legends, and become the top Dragon Master in PvP battles full of adventure!"
    )


@pytest.mark.asyncio
async def test_unit_content_scraper_finds_app_release_date(
    page_data: dict[str, str], scrape_configs: Sites
) -> None:
    output = await scrape_aptoid_content(page_data, scrape_configs, "appReleaseDate")
    assert output == "(\n\n05-06-2024\n\n)"


@pytest.mark.asyncio
async def test_unit_content_scraper_does_not_find_value(
    page_data: dict[str, str], scrape_configs: Sites
) -> None:
    scrape_configs.aptoid.xpath.app_name = "invalid"
    with pytest.raises(HtmlParsingError) as exc:
        await scrape_aptoid_content(page_data, scrape_configs, "appName")
    assert exc.value.partial_data == {"appName": ""}
