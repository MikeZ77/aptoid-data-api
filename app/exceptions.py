import falcon
from falcon import App, Request, Response


class ValidationError(Exception):
    def __init__(self, message: str):
        self.message = message


class ValidationHandler(ValidationError):
    @staticmethod
    async def handler(req: Request, resp: Response, exc: ValidationError, params):
        # TODO: Log the error
        raise falcon.HTTPError(falcon.HTTP_400, description=exc.message)


def register_exception_handlers(app: App):
    app.add_error_handler(ValidationError, ValidationHandler.handler)
