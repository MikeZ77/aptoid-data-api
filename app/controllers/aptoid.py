import aiohttp
import falcon
import falcon.errors
from falcon import Request, Response

from app.domain.scraper import ContentScraper
from app.middleware.validators import validate_url
from app.utils.logger import logger


class AptoidResource:
    def __init__(self, config: dict[str, str]):
        self.logger = logger
        self.config = config

    @falcon.before(validate_url)
    async def on_get(self, req: Request, resp: Response):
        app_url = req.params.get("url")
        xpath = self.config.get("xpath")

        async with aiohttp.ClientSession() as session:
            data = await ContentScraper(xpath, session)(app_url)

        resp.media = data
