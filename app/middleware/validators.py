import re

import validators
from falcon import Request, Response
from falcon.uri import parse_query_string

from app.utils.exceptions import ValidationError


async def validate_url(req: Request, res: Response, resource, params: dict):
    url = parse_query_string(req.query_string).get("url")
    domain = resource.config.get("domain")

    if not validators.url(url) or not re.match(
        rf"https?://[a-zA-Z0-9-]+\.{domain}/.*", url
    ):
        raise ValidationError(f"Please provide a valid url for {domain}.")
