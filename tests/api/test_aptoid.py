import httpx
from falcon.uri import encode

from app.utils.general import load_scrape_configs
from tests.conftest import API_BASE_URL

RESOURCE = "/api/v1/aptoid"
URL = encode("https://dragon-city.en.aptoide.com/app")

description = "Ready to master one of your favorite dragon games? Download \
Dragon City Mobile to fight and feed adorable fire-breathing dragons in this epic \
PvP adventure!\n\nBuild floating islands in Dragon City Mobile, fill it with farms, \
habitats, buildings…and tons of dragons! Train them up, feed and evolve them into \
beasts of legends, and become the top Dragon Master in PvP battles full of adventure!"


def test_api_aptoid_get() -> None:
    response = httpx.get(f"{API_BASE_URL}{RESOURCE}?url={URL}")
    output = response.json()
    output["appDescription"] = output["appDescription"][: len(description)]
    assert response.status_code == 200
    assert output == {
        "appName": "Dragon City",
        "appVersion": "24.6.0",
        "appDownloads": "4M+",
        "appReleaseDate": "(\n\n05-06-2024\n\n)",
        "appDescription": description,
    }


def test_api_aptoid_get_invalid_url() -> None:
    invalid_url = URL.replace("https", "")
    domain = load_scrape_configs().aptoid.domain
    response = httpx.get(f"{API_BASE_URL}{RESOURCE}?url={invalid_url}")
    assert response.status_code == 400
    assert response.json() == {
        "title": "400 Bad Request",
        "description": f"Please provide a valid url for {domain}.",
    }


def test_api_aptoid_app_not_found() -> None:
    invalid_app = URL.replace("dragon-city", "invalid")
    response = httpx.get(f"{API_BASE_URL}{RESOURCE}?url={invalid_app}")
    assert response.status_code == 400
    assert response.json() == {
        "title": f"App for {invalid_app} is not found. Please check the URL",
    }
