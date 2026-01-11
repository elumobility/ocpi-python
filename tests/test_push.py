import asyncio
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


@patch(
    "ocpi.core.push.httpx.AsyncClient",
    side_effect=MockAsyncClientGeneratorVersionsAndEndpoints,
)
def test_push_partial_object(async_client):
    """Test PATCH push functionality for partial updates."""
    from ocpi.core.push import push_partial_object
    from ocpi.core.schemas import Push, Receiver

    adapter = MagicMock()

    # Create a push request for partial update
    push = Push(
        module_id=enums.ModuleID.locations,
        object_id="location-123",
        receivers=[
            Receiver(
                endpoints_url="http://example.com/ocpi/2.3.0/details",
                auth_token="token",
            ),
        ],
    )

    # Partial update data (only changed fields)
    partial_data = {
        "status": "CHARGING",
        "last_updated": "2024-01-10T12:00:00Z",
    }

    # Test PATCH for location
    result = asyncio.run(
        push_partial_object(
            version=VersionNumber.v_2_3_0,
            push=push,
            partial_data=partial_data,
            adapter=adapter,
        )
    )

    # Verify response structure
    assert result is not None
    assert hasattr(result, "receiver_responses")
    assert len(result.receiver_responses) == 1
    assert result.receiver_responses[0].status_code == 200

    # Verify adapter was NOT called (PATCH uses partial data directly)
    adapter.location_adapter.assert_not_called()


@patch(
    "ocpi.core.push.httpx.AsyncClient",
    side_effect=MockAsyncClientGeneratorVersionsAndEndpoints,
)
def test_push_partial_object_with_evse(async_client):
    """Test PATCH push functionality for EVSE partial updates."""
    from ocpi.core.push import push_partial_object
    from ocpi.core.schemas import Push, Receiver

    adapter = MagicMock()

    # Create a push request for EVSE partial update
    push = Push(
        module_id=enums.ModuleID.locations,
        object_id="location-123",
        receivers=[
            Receiver(
                endpoints_url="http://example.com/ocpi/2.3.0/details",
                auth_token="token",
            ),
        ],
    )

    # Partial update data for EVSE status change
    partial_data = {
        "status": "CHARGING",
        "last_updated": "2024-01-10T12:00:00Z",
    }

    # Test PATCH for EVSE (with evse_uid)
    result = asyncio.run(
        push_partial_object(
            version=VersionNumber.v_2_3_0,
            push=push,
            partial_data=partial_data,
            adapter=adapter,
            evse_uid="evse-123",
        )
    )

    # Verify response structure
    assert result is not None
    assert hasattr(result, "receiver_responses")
    assert len(result.receiver_responses) == 1
    assert result.receiver_responses[0].status_code == 200

    # Verify adapter was NOT called (PATCH uses partial data directly)
    adapter.location_adapter.assert_not_called()


@patch(
    "ocpi.core.push.httpx.AsyncClient",
    side_effect=MockAsyncClientGeneratorVersionsAndEndpoints,
)
def test_push_object_with_patch_flag(async_client):
    """Test push_object with use_patch=True flag."""
    from ocpi.core.push import push_object
    from ocpi.core.schemas import Push, Receiver

    adapter = MagicMock()

    # Create a push request
    push = Push(
        module_id=enums.ModuleID.locations,
        object_id="location-123",
        receivers=[
            Receiver(
                endpoints_url="http://example.com/ocpi/2.3.0/details",
                auth_token="token",
            ),
        ],
    )

    # Partial update data
    partial_data = {
        "name": "Updated Location Name",
        "last_updated": "2024-01-10T12:00:00Z",
    }

    # Test push_object with use_patch=True
    result = asyncio.run(
        push_object(
            version=VersionNumber.v_2_3_0,
            push=push,
            crud=None,  # Not needed for PATCH
            adapter=adapter,
            use_patch=True,
            partial_data=partial_data,
        )
    )

    # Verify response structure
    assert result is not None
    assert hasattr(result, "receiver_responses")
    assert len(result.receiver_responses) == 1
    assert result.receiver_responses[0].status_code == 200

    # Verify adapter was NOT called (PATCH uses partial data directly)
    adapter.location_adapter.assert_not_called()


@patch(
    "ocpi.core.push.httpx.AsyncClient",
    side_effect=MockAsyncClientGeneratorVersionsAndEndpoints,
)
def test_push_object_with_connector(async_client):
    """Test PATCH push functionality for Connector partial updates."""
    from ocpi.core.push import push_partial_object
    from ocpi.core.schemas import Push, Receiver

    adapter = MagicMock()

    # Create a push request for Connector partial update
    push = Push(
        module_id=enums.ModuleID.locations,
        object_id="location-123",
        receivers=[
            Receiver(
                endpoints_url="http://example.com/ocpi/2.3.0/details",
                auth_token="token",
            ),
        ],
    )

    # Partial update data for Connector (e.g., tariff update)
    partial_data = {
        "tariff_ids": ["15"],
        "last_updated": "2024-01-10T12:00:00Z",
    }

    # Test PATCH for Connector (with evse_uid and connector_id)
    result = asyncio.run(
        push_partial_object(
            version=VersionNumber.v_2_3_0,
            push=push,
            partial_data=partial_data,
            adapter=adapter,
            evse_uid="evse-123",
            connector_id="connector-1",
        )
    )

    # Verify response structure
    assert result is not None
    assert hasattr(result, "receiver_responses")
    assert len(result.receiver_responses) == 1
    assert result.receiver_responses[0].status_code == 200

    # Verify adapter was NOT called (PATCH uses partial data directly)
    adapter.location_adapter.assert_not_called()
