from __future__ import annotations

from pydantic import BaseModel, Field


class Sites(BaseModel):
    aptoid: SiteDetails


class SiteDetails(BaseModel):
    domain: str
    xpath: AptoidXpath
    endpoint_tests: list[str]


class AptoidXpath(BaseModel):
    app_name: str = Field(alias="appName")
    app_version: str = Field(alias="appVersion")
    app_downloads: str = Field(alias="appDownloads")
    app_release_date: str = Field(alias="appReleaseDate")
    app_description: str = Field(alias="appDescription")
