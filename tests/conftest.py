import time
from pathlib import Path
from typing import Any, Generator

import docker
import httpx
import pytest
from _pytest.fixtures import SubRequest
from _pytest.python import Function
from lxml import html

from app.config.models import Sites
from app.utils.general import load_scrape_configs, project_root

API_BASE_URL = "http://127.0.0.1:8000"


@pytest.fixture
def page_data() -> dict[str, html.HtmlElement]:
    # TODO: Load in configs using pydantic models
    pages = Path(__file__).parent / "pages"
    data = {}

    for page in pages.iterdir():
        if page.suffix != ".html":
            continue

        with open(page) as f:
            html_str = f.read()
            data[page.stem] = html_str

    return data


@pytest.fixture
def scrape_configs() -> Sites:
    return load_scrape_configs()


def pytest_collection_modifyitems(items: list[Function]) -> None:
    for test_fn in items:
        if "test_integration_" in test_fn.name:
            test_fn.add_marker(pytest.mark.integration)

        if "test_api_" in test_fn.name:
            test_fn.add_marker(pytest.mark.api)

        if "test_unit_" in test_fn.name:
            test_fn.add_marker(pytest.mark.unit)


def is_api_ready(attempts: int = 5, delay: int = 5) -> None:
    while attempts:
        try:
            httpx.get(API_BASE_URL + "/health").raise_for_status()
            return
        except Exception:
            attempts -= 1
            time.sleep(delay)


@pytest.fixture(scope="session", autouse=True)
def bring_up_app(request: SubRequest) -> Generator[None, Any, None]:
    has_api_test = False
    for test_fn in request.session.items:
        for marker in test_fn.own_markers:
            if marker.name == "api":
                has_api_test = True

    if has_api_test:
        client = docker.from_env()
        client.images.build(path=project_root().as_posix(), tag="web-scraper")
        container = client.containers.run(
            "web-scraper", detach=True, ports={"8000": 8000}
        )
        is_api_ready()

    yield

    if has_api_test:
        container.stop()
        container.remove()
