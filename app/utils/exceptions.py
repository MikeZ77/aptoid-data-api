import falcon
from falcon import App, Request, Response


class BaseException(Exception):
    def __init__(self, message: str):
        self.message = message


class ValidationError(BaseException): ...


class HtmlParsingError(Exception):
    def __init__(self, message: str, partial_data: dict[str, str | None]):
        self.message = message
        self.partial_data = partial_data


class ValidationHandler(ValidationError):
    @staticmethod
    async def handler(req: Request, resp: Response, exc: ValidationError, params):
        raise falcon.HTTPError(falcon.HTTP_400, description=exc.message)


class HtmlParsingErrorHandler(HtmlParsingError):
    @staticmethod
    async def handler(req: Request, resp: Response, exc: HtmlParsingError, params):
        raise falcon.HTTPError(
            falcon.HTTP_500, description=exc.message, partialData=exc.partial_data
        )


def register_exception_handlers(app: App):
    app.add_error_handler(ValidationError, ValidationHandler.handler)
    app.add_error_handler(HtmlParsingError, HtmlParsingErrorHandler.handler)
