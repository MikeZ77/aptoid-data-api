import asyncio

import aiohttp

from app.domain.scraper import ContentScraper
from app.utils.general import load_scrape_configs
from app.utils.logger import logger


async def _fetch_content(endpoint: str, xpath: dict[str, str]) -> None:
    missing_data = None
    try:
        async with aiohttp.ClientSession() as session:
            output = await ContentScraper(xpath, session)(endpoint)
            missing_data = {attr: data for attr, data in output.items() if not data}

    except Exception as e:
        logger.error(f"Error checking endpoint {endpoint}: {str(e)}")

    if missing_data:
        logger.error(f"Missing data for endpoint {endpoint}: {missing_data}")


async def alert_endpoints(wait: int = 20) -> None:
    configs = load_scrape_configs()
    endpoints = configs.aptoid.endpoint_tests
    xpath = configs.aptoid.xpath.model_dump(by_alias=True)

    while True:
        for endpoint in endpoints:
            logger.info(f"Checking endpoint: {endpoint}")
            await _fetch_content(endpoint, xpath)
            await asyncio.sleep(wait)
