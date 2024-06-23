from falcon import Request, Response


class HealthResource:
    async def on_get(self, req: Request, resp: Response) -> None:
        resp.text = "API is up and running!"
