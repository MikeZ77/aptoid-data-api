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
