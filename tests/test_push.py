from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4

from fastapi.testclient import TestClient

from ocpi import get_application
from ocpi.core import enums, schemas
from ocpi.modules.locations.v_2_2_1.schemas import Location
from ocpi.modules.versions.enums import VersionNumber
from tests.test_modules.mocks.async_client import (
    MockAsyncClientGeneratorVersionsAndEndpoints,
)
from tests.test_modules.utils import (
    ENCODED_AUTH_TOKEN,
    ClientAuthenticator,
)

LOCATIONS = [
    {
        "country_code": "us",
        "party_id": "AAA",
        "id": str(uuid4()),
        "publish": True,
        "publish_allowed_to": [
            {
                "uid": str(uuid4()),
                "type": "APP_USER",
                "visual_number": "1",
                "issuer": "issuer",
                "group_id": "group_id",
            },
        ],
        "name": "name",
        "address": "address",
        "city": "city",
        "postal_code": "111111",
        "state": "state",
        "country": "USA",
        "coordinates": {
            "latitude": "latitude",
            "longitude": "longitude",
        },
        "related_locations": [
            {
                "latitude": "latitude",
                "longitude": "longitude",
                "name": {"language": "en", "text": "name"},
            },
        ],
        "parking_type": "ON_STREET",
        "evses": [
            {
                "uid": str(uuid4()),
                "evse_id": str(uuid4()),
                "status": "AVAILABLE",
                "status_schedule": {
                    "period_begin": "2022-01-01T00:00:00+00:00",
                    "period_end": "2022-01-01T00:00:00+00:00",
                    "status": "AVAILABLE",
                },
                "capabilities": [
                    "CREDIT_CARD_PAYABLE",
                ],
                "connectors": [
                    {
                        "id": str(uuid4()),
                        "standard": "DOMESTIC_A",
                        "format": "SOCKET",
                        "power_type": "DC",
                        "max_voltage": 100,
                        "max_amperage": 100,
                        "max_electric_power": 100,
                        "tariff_ids": [
                            str(uuid4()),
                        ],
                        "terms_and_conditions": "https://www.example.com",
                        "last_updated": "2022-01-01T00:00:00+00:00",
                    }
                ],
                "floor_level": "3",
                "coordinates": {
                    "latitude": "latitude",
                    "longitude": "longitude",
                },
                "physical_reference": "pr",
                "directions": [
                    {"language": "en", "text": "directions"},
                ],
                "parking_restrictions": [
                    "EV_ONLY",
                ],
                "images": [
                    {
                        "url": "https://www.example.com",
                        "thumbnail": "https://www.example.com",
                        "category": "CHARGER",
                        "type": "type",
                        "width": 10,
                        "height": 10,
                    },
                ],
                "last_updated": "2022-01-01T00:00:00+00:00",
            }
        ],
        "directions": [
            {"language": "en", "text": "directions"},
        ],
        "operator": {
            "name": "name",
            "website": "https://www.example.com",
            "logo": {
                "url": "https://www.example.com",
                "thumbnail": "https://www.example.com",
                "category": "CHARGER",
                "type": "type",
                "width": 10,
                "height": 10,
            },
        },
        "suboperator": {
            "name": "name",
            "website": "https://www.example.com",
            "logo": {
                "url": "https://www.example.com",
                "thumbnail": "https://www.example.com",
                "category": "CHARGER",
                "type": "type",
                "width": 10,
                "height": 10,
            },
        },
        "owner": {
            "name": "name",
            "website": "https://www.example.com",
            "logo": {
                "url": "https://www.example.com",
                "thumbnail": "https://www.example.com",
                "category": "CHARGER",
                "type": "type",
                "width": 10,
                "height": 10,
            },
        },
        "facilities": ["MALL"],
        "time_zone": "UTC+2",
        "opening_times": {
            "twentyfourseven": True,
            "regular_hours": [
                {
                    "weekday": 1,
                    "period_begin": "8:00",
                    "period_end": "22:00",
                },
                {
                    "weekday": 2,
                    "period_begin": "8:00",
                    "period_end": "22:00",
                },
            ],
            "exceptional_openings": [
                {
                    "period_begin": "2022-01-01T00:00:00+00:00",
                    "period_end": "2022-01-02T00:00:00+00:00",
                },
            ],
            "exceptional_closings": [],
        },
        "charging_when_closed": False,
        "images": [
            {
                "url": "https://www.example.com",
                "thumbnail": "https://www.example.com",
                "category": "CHARGER",
                "type": "type",
                "width": 10,
                "height": 10,
            },
        ],
        "energy_mix": {
            "is_green_energy": True,
            "energy_sources": [
                {"source": "SOLAR", "percentage": 100},
            ],
            "environ_impact": None,
            "supplier_name": "supplier_name",
            "energy_product_name": "energy_product_name",
        },
        "last_updated": "2022-01-02 00:00:00+00:00",
    }
]


@patch(
    "ocpi.core.push.httpx.AsyncClient",
    side_effect=MockAsyncClientGeneratorVersionsAndEndpoints,
)
def test_push(async_client):
    crud = AsyncMock()
    adapter = MagicMock()

    crud.get.return_value = LOCATIONS[0]
    adapter.location_adapter.return_value = Location(**LOCATIONS[0])

    app = get_application(
        version_numbers=[VersionNumber.v_2_2_1],
        roles=[enums.RoleEnum.cpo],
        crud=crud,
        adapter=adapter,
        authenticator=ClientAuthenticator,
        modules=[],
        http_push=True,
    )

    client = TestClient(app)
    data = schemas.Push(
        module_id=enums.ModuleID.locations,
        object_id="1",
        receivers=[
            schemas.Receiver(endpoints_url="http://example.com", auth_token="token"),
        ],
    ).model_dump()
    client.post(
        "/push/2.2.1",
        json=data,
        headers={"Authorization": f"Token {ENCODED_AUTH_TOKEN}"},
    )

    crud.get.assert_awaited_once()
    adapter.location_adapter.assert_called_once()


def test_http_push_to_client():
    """Test http_push_to_client endpoint."""
    from unittest.mock import AsyncMock, MagicMock, patch

    crud = AsyncMock()
    adapter = MagicMock()

    crud.get.return_value = {"id": "loc-123"}
    adapter.location_adapter.return_value.model_dump.return_value = {"id": "loc-123"}

    app = get_application(
        version_numbers=[VersionNumber.v_2_2_1],
        roles=[enums.RoleEnum.cpo],
        crud=crud,
        adapter=adapter,
        authenticator=ClientAuthenticator,
        modules=[],
        http_push=True,
    )

    client = TestClient(app)
    push_data = schemas.Push(
        module_id=enums.ModuleID.locations,
        object_id="loc-123",
        receivers=[
            schemas.Receiver(
                endpoints_url="http://example.com/versions", auth_token="token"
            ),
        ],
    ).model_dump()

    # Mock the endpoints and push responses
    with patch("ocpi.core.push.httpx.AsyncClient") as mock_client:
        # Mock endpoints response
        mock_endpoints_response = MagicMock()
        mock_endpoints_response.status_code = 200
        mock_endpoints_response.json.return_value = {
            "data": {
                "endpoints": [
                    {
                        "identifier": enums.ModuleID.locations,
                        "role": "RECEIVER",
                        "url": "http://example.com/locations",
                    }
                ]
            }
        }

        # Mock push response
        mock_push_response = MagicMock()
        mock_push_response.status_code = 200
        mock_push_response.json.return_value = {"status_code": 1000}

        mock_client.return_value.__aenter__.return_value.get = AsyncMock(
            return_value=mock_endpoints_response
        )
        mock_client.return_value.__aenter__.return_value.send = AsyncMock(
            return_value=mock_push_response
        )
        mock_client.return_value.__aenter__.return_value.build_request = MagicMock()

        response = client.post(
            "/push/2.2.1",
            json=push_data,
            headers={"Authorization": f"Token {ENCODED_AUTH_TOKEN}"},
        )

    assert response.status_code == 200


def test_http_push_unauthenticated():
    """Push endpoint returns 422 when Authorization header is missing entirely
    (FastAPI rejects the request before auth logic runs)."""
    app = get_application(
        version_numbers=[VersionNumber.v_2_2_1],
        roles=[enums.RoleEnum.cpo],
        crud=AsyncMock(),
        adapter=MagicMock(),
        authenticator=ClientAuthenticator,
        modules=[],
        http_push=True,
    )

    client = TestClient(app)
    push_data = schemas.Push(
        module_id=enums.ModuleID.locations,
        object_id="loc-1",
        receivers=[
            schemas.Receiver(endpoints_url="http://example.com", auth_token="token"),
        ],
    ).model_dump()

    response = client.post("/push/2.2.1", json=push_data)
    assert response.status_code == 422


def test_http_push_wrong_token():
    """Push endpoint returns 403 when wrong token is provided."""
    from tests.test_modules.utils import ENCODED_RANDOM_AUTH_TOKEN

    app = get_application(
        version_numbers=[VersionNumber.v_2_2_1],
        roles=[enums.RoleEnum.cpo],
        crud=AsyncMock(),
        adapter=MagicMock(),
        authenticator=ClientAuthenticator,
        modules=[],
        http_push=True,
    )

    client = TestClient(app)
    push_data = schemas.Push(
        module_id=enums.ModuleID.locations,
        object_id="loc-1",
        receivers=[
            schemas.Receiver(endpoints_url="http://example.com", auth_token="token"),
        ],
    ).model_dump()

    response = client.post(
        "/push/2.2.1",
        json=push_data,
        headers={"Authorization": f"Token {ENCODED_RANDOM_AUTH_TOKEN}"},
    )
    assert response.status_code == 403


def test_push_cdr_module():
    """Push with CDR module uses POST and base_url directly (no object_id appended)."""
    crud = AsyncMock()
    adapter = MagicMock()
    crud.get.return_value = {"id": "cdr-1"}
    adapter.cdr_adapter.return_value.model_dump.return_value = {"id": "cdr-1"}

    app = get_application(
        version_numbers=[VersionNumber.v_2_2_1],
        roles=[enums.RoleEnum.cpo],
        crud=crud,
        adapter=adapter,
        authenticator=ClientAuthenticator,
        modules=[],
        http_push=True,
    )

    client = TestClient(app)
    push_data = schemas.Push(
        module_id=enums.ModuleID.cdrs,
        object_id="cdr-1",
        receivers=[
            schemas.Receiver(
                endpoints_url="http://example.com/versions", auth_token="token"
            ),
        ],
    ).model_dump()

    with patch("ocpi.core.push.httpx.AsyncClient") as mock_client:
        mock_endpoints_response = MagicMock()
        mock_endpoints_response.status_code = 200
        mock_endpoints_response.json.return_value = {
            "data": {
                "endpoints": [
                    {
                        "identifier": enums.ModuleID.cdrs,
                        "role": "RECEIVER",
                        "url": "http://example.com/cdrs/",
                    }
                ]
            }
        }

        mock_push_response = MagicMock()
        mock_push_response.status_code = 200
        mock_push_response.headers = {"Location": "http://example.com/cdrs/cdr-1"}

        mock_client.return_value.__aenter__.return_value.get = AsyncMock(
            return_value=mock_endpoints_response
        )
        mock_client.return_value.__aenter__.return_value.send = AsyncMock(
            return_value=mock_push_response
        )
        mock_client.return_value.__aenter__.return_value.build_request = MagicMock()

        response = client.post(
            "/push/2.2.1",
            json=push_data,
            headers={"Authorization": f"Token {ENCODED_AUTH_TOKEN}"},
        )

    assert response.status_code == 200
    # For CDR, build_request should use POST
    call_args = mock_client.return_value.__aenter__.return_value.build_request.call_args
    assert call_args[0][0] == "POST"


def test_push_token_module_uses_emsp_role():
    """Push with tokens module fetches data using EMSP role."""
    crud = AsyncMock()
    adapter = MagicMock()
    crud.get.return_value = {"uid": "tok-1"}
    adapter.token_adapter.return_value.model_dump.return_value = {"uid": "tok-1"}

    app = get_application(
        version_numbers=[VersionNumber.v_2_2_1],
        roles=[enums.RoleEnum.cpo],
        crud=crud,
        adapter=adapter,
        authenticator=ClientAuthenticator,
        modules=[],
        http_push=True,
    )

    client = TestClient(app)
    push_data = schemas.Push(
        module_id=enums.ModuleID.tokens,
        object_id="tok-1",
        receivers=[
            schemas.Receiver(
                endpoints_url="http://example.com/versions", auth_token="token"
            ),
        ],
    ).model_dump()

    with patch("ocpi.core.push.httpx.AsyncClient") as mock_client:
        mock_endpoints_response = MagicMock()
        mock_endpoints_response.status_code = 200
        mock_endpoints_response.json.return_value = {
            "data": {
                "endpoints": [
                    {
                        "identifier": enums.ModuleID.tokens,
                        "role": "RECEIVER",
                        "url": "http://example.com/tokens/",
                    }
                ]
            }
        }

        mock_push_response = MagicMock()
        mock_push_response.status_code = 200
        mock_push_response.json.return_value = {"status_code": 1000}

        mock_client.return_value.__aenter__.return_value.get = AsyncMock(
            return_value=mock_endpoints_response
        )
        mock_client.return_value.__aenter__.return_value.send = AsyncMock(
            return_value=mock_push_response
        )
        mock_client.return_value.__aenter__.return_value.build_request = MagicMock()

        client.post(
            "/push/2.2.1",
            json=push_data,
            headers={"Authorization": f"Token {ENCODED_AUTH_TOKEN}"},
        )

    # Tokens module should fetch with EMSP role
    crud.get.assert_awaited_once()
    call_kwargs = crud.get.call_args
    assert call_kwargs[0][1] == enums.RoleEnum.emsp
