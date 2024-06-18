import falcon
from falcon import Request, Response

from app.domain.aptoid import Aptoid
from app.middleware.validators import validate_get_aptoid
from app.utils.logger import logger
from app.utils.requests import HttpRequests


class AptoidResource:
    def __init__(self):
        self.logger = logger

    @falcon.before(validate_get_aptoid)
    async def on_get(self, req: Request, resp: Response):
        Aptoid(HttpRequests())
        resp.status = falcon.HTTP_200
        # TODO: use pydantic to convert snake case to camel case
        resp.media = {
            "appName": "TestApp",
            "appVersion": "1.0.0",
            "appDownloads": 100,
            "appReleaseDate": "10/20/2023",
            "appDescription": "This is some description text",
        }

    async def on_post(self, req: Request, resp: Response):
        resp.status = falcon.HTTP_200
