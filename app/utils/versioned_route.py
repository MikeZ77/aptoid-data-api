from falcon import App


# TODO: Create a type for all our resources
def add_versioned_route(self: App, version: int, route: str, resource):
    prefixed_route = f"/api/v{version}{route}"
    self.add_route(prefixed_route, resource)
