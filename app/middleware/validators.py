import validators
from falcon import Request, Response
from falcon.uri import parse_query_string

from app.exceptions import ValidationError


async def validate_get_aptoid(req: Request, res: Response, resource, params: dict):
    query_params = parse_query_string(req.query_string)
    if not validators.url(query_params.get("app_url")):
        raise ValidationError("Please provide a valid url for the Aproide app store.")
