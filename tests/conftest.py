from pathlib import Path

import docker
import pytest
from _pytest.fixtures import SubRequest
from _pytest.python import Function
from lxml import html

from app.utils.general import load_scrape_configs, project_root


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
def scrape_configs() -> dict:
    return load_scrape_configs()


def pytest_collection_modifyitems(items: list[Function]):
    for test_fn in items:
        if "test_integration_" in test_fn.name:
            test_fn.add_marker(pytest.mark.integration)

        if "test_api_" in test_fn.name:
            test_fn.add_marker(pytest.mark.api)

        if "test_unit_" in test_fn.name:
            test_fn.add_marker(pytest.mark.unit)


@pytest.fixture(scope="session", autouse=True)
def bring_up_app(request: SubRequest):
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

    yield

    if has_api_test:
        container.stop()
        container.remove()
