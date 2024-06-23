import falcon
from falcon import App, Request, Response

from app.utils.types import Params


class BaseException(Exception):
    def __init__(self, message: str):
        self.message = message


class ValidationError(BaseException): ...


class HtmlParsingError(Exception):
    def __init__(self, partial_data: dict[str, str]):
        self.partial_data = partial_data
        self.message = f"""Missing values could not be found in HTML: 
            {[data for data, value in partial_data.items() if not value]}
        """


class ValidationHandler(ValidationError):
    @staticmethod
    async def handler(
        req: Request, resp: Response, exc: ValidationError, params: Params
    ) -> None:
        raise falcon.HTTPError(falcon.HTTP_400, description=exc.message)


class HtmlParsingErrorHandler(HtmlParsingError):
    @staticmethod
    async def handler(
        req: Request, resp: Response, exc: HtmlParsingError, params: Params
    ) -> None:
        raise falcon.HTTPError(
            falcon.HTTP_500, description=exc.message, partialData=exc.partial_data
        )


def register_exception_handlers(app: App) -> None:
    app.add_error_handler(ValidationError, ValidationHandler.handler)
    app.add_error_handler(HtmlParsingError, HtmlParsingErrorHandler.handler)
