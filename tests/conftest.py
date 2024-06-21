from pathlib import Path

import pytest
from lxml import html

from app.utils.general import load_scrape_configs


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
