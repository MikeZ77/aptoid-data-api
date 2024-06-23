import asyncio

from falcon.asgi import App

from app.controllers.aptoid import AptoidResource
from app.controllers.health import HealthResource
from app.services.alert_endpoints import alert_endpoints
from app.utils.exceptions import register_exception_handlers
from app.utils.general import add_versioned_route, load_scrape_configs, project_root

App.add_versioned_route = add_versioned_route
app = App()
register_exception_handlers(app)
config = load_scrape_configs()

templates = project_root() / "app/client"
app.add_static_route("/", templates)
app.add_route("/health", HealthResource())
app.add_versioned_route(
    version=1, route="/aptoid", resource=AptoidResource(config.aptoid)
)

asyncio.create_task(alert_endpoints())
