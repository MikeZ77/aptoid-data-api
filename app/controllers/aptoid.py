import aiohttp
import falcon
import falcon.errors
from falcon import Request, Response

from app.config.models import SiteDetails
from app.domain.scraper import ContentScraper
from app.middleware.validators import validate_url
from app.utils.logger import logger


class AptoidResource:
    def __init__(self, config: SiteDetails):
        self.logger = logger
        self.config = config

    @falcon.before(validate_url)  # type: ignore
    async def on_get(self, req: Request, resp: Response) -> None:
        app_url = req.params.get("url")
        xpath = self.config.xpath.model_dump(by_alias=True)

        async with aiohttp.ClientSession() as session:
            data = await ContentScraper(xpath, session)(app_url)

        resp.media = data


# NOTE: falcon.before does not have typing so mypy throws an error for on_get.
# This could be solved by creating a typed decorator factory around falcon.before
# but the typing would still be complex.
