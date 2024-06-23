from logging import Logger
from typing import Protocol

from falcon import Request, Response

from app.config.models import SiteDetails


class Resource(Protocol):
    logger: Logger
    config: SiteDetails

    def on_get(self, req: Request, resp: Response) -> None: ...

    def on_post(self, req: Request, resp: Response) -> None: ...

    def on_put(self, req: Request, resp: Response) -> None: ...

    def on_delete(self, req: Request, resp: Response) -> None: ...
