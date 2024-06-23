import json
from pathlib import Path

from falcon import App

from app.config.models import Sites
from app.controllers.protocol import Resource


def add_versioned_route(
    self: App, version: int, route: str, resource: Resource
) -> None:
    prefixed_route = f"/api/v{version}{route}"
    self.add_route(prefixed_route, resource)


def project_root() -> Path:
    return Path(__file__).parent.parent.parent


def load_scrape_configs() -> Sites:
    # NOTE: The point of loading in the xpath as config is so that later on this
    # can be stored in the database. This would allow "hot reload" behind a protected
    # endpoint like /config/reload.
    with open(project_root() / "app/config/sites.json") as config:
        return Sites(**json.load(config))
