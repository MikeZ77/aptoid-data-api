from pathlib import Path

from falcon.asgi import App

from app.controllers.aptoid import AptoidResource
from app.exceptions import register_exception_handlers
from app.utils.versioned_route import add_versioned_route

# TODO: Load version from env
App.add_versioned_route = add_versioned_route
app = App()
register_exception_handlers(app)


# TODO: Add Redis middleware for caching
# TODO Add request and response logging middleware

templates = Path(__file__).parent / "client"
app.add_static_route("/", templates)
app.add_versioned_route(version=1, route="/aptoid", resource=AptoidResource())
