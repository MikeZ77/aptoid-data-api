import httpx
from falcon.uri import encode

FQDN = "http://127.0.0.1:8000/api/v1/aptoid"
URL = encode("https://dragon-city.en.aptoide.com/app")

description = "Ready to master one of your favorite dragon games? Download \
Dragon City Mobile to fight and feed adorable fire-breathing dragons in this epic \
PvP adventure!\n\nBuild floating islands in Dragon City Mobile, fill it with farms, \
habitats, buildings…and tons of dragons! Train them up, feed and evolve them into \
beasts of legends, and become the top Dragon Master in PvP battles full of adventure!"


def test_api_aptoid_get():
    response = httpx.get(f"{FQDN}?url={URL}")
    output = response.json()
    output["appReleaseDate"] = output["appReleaseDate"][: len(description)]
    assert response.status_code == 200
    assert output == {
        "appName": "Dragon City",
        "appVersion": "24.6.0",
        "appDownloads": "4M+",
        "appReleaseDate": "(\n\n05-06-2024\n\n)",
        "appDescription": description,
    }
