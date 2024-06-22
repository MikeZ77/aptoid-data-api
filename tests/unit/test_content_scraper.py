import pytest

from app.domain.scraper import ContentScraper


class MockRequestContextManager:
    def __init__(self, response: str):
        self.response = response

    async def __aenter__(self):
        return self

    async def __aexit__(self, *_args):
        pass

    async def text(self):
        return self.response


class MockClientSession:
    def __init__(self, response: str):
        self.response = response

    def get(self, _: str):
        return MockRequestContextManager(self.response)


async def scrape_aptoid_content(
    page_data: dict[str, str], scrape_configs: dict, value: str
) -> str:
    html = page_data["aptoid_dragon_city"]
    aptoid_xpath = scrape_configs["aptoid"]["xpath"]
    xpath = {xpath: query for xpath, query in aptoid_xpath.items() if xpath == value}
    return (await ContentScraper(xpath, MockClientSession(html))(""))[value]


@pytest.mark.asyncio
async def test_unit_content_scraper_finds_app_name(
    page_data: dict[str, str], scrape_configs: dict
):
    output = await scrape_aptoid_content(page_data, scrape_configs, "appName")
    assert output == "Dragon City"


@pytest.mark.asyncio
async def test_unit_content_scraper_finds_app_version(
    page_data: dict[str, str], scrape_configs: dict
):
    output = await scrape_aptoid_content(page_data, scrape_configs, "appVersion")
    assert output == "24.6.0"


@pytest.mark.asyncio
async def test_unit_content_scraper_finds_app_downloads(
    page_data: dict[str, str], scrape_configs: dict
):
    output = await scrape_aptoid_content(page_data, scrape_configs, "appDownloads")
    assert output == "4M+"


@pytest.mark.asyncio
async def test_unit_content_scraper_finds_app_description(
    page_data: dict[str, str], scrape_configs: dict
):
    output = await scrape_aptoid_content(page_data, scrape_configs, "appDescription")
    assert (
        output
        == "Ready to master one of your favorite dragon games? Download \
Dragon City Mobile to fight and feed adorable fire-breathing dragons in this epic \
PvP adventure!\n\nBuild floating islands in Dragon City Mobile, fill it with farms, \
habitats, buildings…and tons of dragons! Train them up, feed and evolve them into \
beasts of legends, and become the top Dragon Master in PvP battles full of adventure!"
    )
