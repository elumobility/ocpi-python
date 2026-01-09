from datetime import datetime

from fastapi import Query

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ocpi.core.adapter import Adapter
from ocpi.core.authentication.authenticator import Authenticator
from ocpi.core.config import settings
from ocpi.core.crud import Crud
from ocpi.core.data_types import URL
from ocpi.modules.versions.enums import VersionNumber
from ocpi.modules.versions.schemas import Version


def get_crud():
    return Crud


def get_adapter():
    return Adapter


def get_authenticator():
    return Authenticator


def get_versions():
    return [
        Version(
            version=VersionNumber.v_2_2_1,
            url=URL(
                f"https://{settings.OCPI_HOST}/{settings.OCPI_PREFIX}/"
                f"{VersionNumber.v_2_2_1.value}/details"
            ),
        ).model_dump(),
    ]


def get_endpoints():
    return {}


def get_modules():
    return []


def pagination_filters(
    date_from: datetime = Query(default=None),
    date_to: datetime = Query(default=None),
    offset: int = Query(default=0),
    limit: int = Query(default=50),
):
    return {
        "date_from": date_from,
        "date_to": date_to,
        "offset": offset,
        "limit": limit,
    }
