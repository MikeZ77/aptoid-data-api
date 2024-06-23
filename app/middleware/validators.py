import re

import validators
from falcon import Request, Response
from falcon.uri import parse_query_string

from app.controllers.protocol import Resource
from app.utils.exceptions import ValidationError
from app.utils.types import Params


async def validate_url(
    req: Request, res: Response, resource: Resource, params: Params
) -> None:
    url = parse_query_string(req.query_string).get("url")
    domain = resource.config.domain

    if not validators.url(url) or not re.match(
        rf"https?://[a-zA-Z0-9-]+\.{domain}/.*", url
    ):
        raise ValidationError(f"Please provide a valid url for {domain}.")
