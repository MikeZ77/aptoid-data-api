import json
from pathlib import Path

from falcon import App


# TODO: Create a type for all our resources
def add_versioned_route(self: App, version: int, route: str, resource):
    prefixed_route = f"/api/v{version}{route}"
    self.add_route(prefixed_route, resource)


def load_scrape_configs() -> dict:
    # NOTE: The way this should work is that the config is stored in a databse and
    # there is a protected endpoint that updates the config and does a hot reload.
    with open(Path(__file__).parent.parent / "config/sites.json") as config:
        return json.load(config)
