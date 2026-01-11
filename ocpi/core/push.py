import httpx
from fastapi import APIRouter, Depends, Request, WebSocket

from ocpi.core.adapter import Adapter
from ocpi.core.authentication.verifier import (
    HttpPushVerifier,
    WSPushVerifier,
)
from ocpi.core.config import logger, settings
from ocpi.core.crud import Crud
from ocpi.core.dependencies import get_adapter, get_crud
from ocpi.core.enums import ModuleID, RoleEnum
from ocpi.core.schemas import Push, PushResponse, ReceiverResponse
from ocpi.core.utils import encode_string_base64, get_auth_token
from ocpi.modules.versions.enums import VersionNumber
from ocpi.modules.versions.v_2_2_1.enums import InterfaceRole as InterfaceRole_2_2_1
from ocpi.modules.versions.v_2_3_0.enums import InterfaceRole as InterfaceRole_2_3_0


def client_url(
    module_id: ModuleID,
    object_id: str,
    base_url: str,
    evse_uid: str | None = None,
    connector_id: str | None = None,
) -> str:
    """
    Build the client URL for push requests.

    Args:
        module_id: The OCPI module ID
        object_id: The object ID (location_id, session_id, etc.)
        base_url: The base URL from endpoint discovery
        evse_uid: Optional EVSE UID for nested location updates
        connector_id: Optional Connector ID for nested location updates

    Returns:
        The full URL for the push request
    """
    if module_id == ModuleID.cdrs:
        return base_url
    url = f"{base_url}{settings.COUNTRY_CODE}/{settings.PARTY_ID}/{object_id}"
    if evse_uid:
        url += f"/{evse_uid}"
    if connector_id:
        url += f"/{connector_id}"
    return url


def client_method(module_id: ModuleID, use_patch: bool = False) -> str:
    """
    Determine the HTTP method for push requests.

    Args:
        module_id: The OCPI module ID
        use_patch: If True, use PATCH instead of PUT

    Returns:
        The HTTP method string ("PUT", "PATCH", or "POST")
    """
    if module_id == ModuleID.cdrs:
        return "POST"
    return "PATCH" if use_patch else "PUT"


def request_data(
    module_id: ModuleID,
    object_data: dict,
    adapter: Adapter,
    version: VersionNumber,
) -> dict:
    data = {}
    if module_id == ModuleID.locations:
        data = adapter.location_adapter(object_data, version).model_dump()
    elif module_id == ModuleID.sessions:
        data = adapter.session_adapter(object_data, version).model_dump()
    elif module_id == ModuleID.cdrs:
        data = adapter.cdr_adapter(object_data, version).model_dump()
    elif module_id == ModuleID.tariffs:
        data = adapter.tariff_adapter(object_data, version).model_dump()
    elif module_id == ModuleID.tokens:
        data = adapter.token_adapter(object_data, version).model_dump()
    return data


async def send_push_request(
    object_id: str,
    object_data: dict,
    module_id: ModuleID,
    adapter: Adapter,
    client_auth_token: str,
    endpoints: list,
    version: VersionNumber,
    use_patch: bool = False,
    evse_uid: str | None = None,
    connector_id: str | None = None,
):
    """
    Send a push request (PUT or PATCH) to the receiver.

    Args:
        object_id: The object ID (location_id, session_id, etc.)
        object_data: The object data (full for PUT, partial for PATCH)
        module_id: The OCPI module ID
        adapter: The adapter to convert data
        client_auth_token: The authorization token
        endpoints: List of endpoints from discovery
        version: OCPI version
        use_patch: If True, send PATCH request (partial update)
        evse_uid: Optional EVSE UID for nested location updates
        connector_id: Optional Connector ID for nested location updates

    Returns:
        HTTP response from the receiver
    """
    # For PATCH, use data directly (it's already partial)
    # For PUT, convert through adapter to ensure full object
    if use_patch:
        data = object_data
    else:
        data = request_data(module_id, object_data, adapter, version)

    base_url = ""
    for endpoint in endpoints:
        if version.value.startswith("2.3"):
            # OCPI 2.3.0 uses InterfaceRole enum
            if (
                endpoint["identifier"] == module_id
                and endpoint["role"] == InterfaceRole_2_3_0.receiver
            ):
                base_url = endpoint["url"]
        elif version.value.startswith("2.2"):
            # OCPI 2.2.x uses InterfaceRole enum
            if (
                endpoint["identifier"] == module_id
                and endpoint["role"] == InterfaceRole_2_2_1.receiver
            ):
                base_url = endpoint["url"]
        elif version.value.startswith("2.1"):
            # OCPI 2.1.x doesn't use InterfaceRole
            if endpoint["identifier"] == module_id:
                base_url = endpoint["url"]

    # push object to client
    async with httpx.AsyncClient() as client:
        request = client.build_request(
            client_method(module_id, use_patch=use_patch),
            client_url(
                module_id,
                object_id,
                base_url,
                evse_uid=evse_uid,
                connector_id=connector_id,
            ),
            headers={"Authorization": client_auth_token},
            json=data,
        )
        response = await client.send(request)
        return response


async def push_object(
    version: VersionNumber,
    push: Push,
    crud: Crud | None,
    adapter: Adapter,
    auth_token: str | None = None,
    use_patch: bool = False,
    partial_data: dict | None = None,
    evse_uid: str | None = None,
    connector_id: str | None = None,
) -> PushResponse:
    """
    Push an object to receivers using PUT (full update) or PATCH (partial update).

    Args:
        version: OCPI version
        push: Push request with module_id, object_id, and receivers
        crud: CRUD adapter to fetch object data (for PUT)
        adapter: Adapter to convert data
        auth_token: Optional auth token for fetching object data
        use_patch: If True, use PATCH method (requires partial_data)
        partial_data: Partial update data (required if use_patch=True)
        evse_uid: Optional EVSE UID for nested location updates
        connector_id: Optional Connector ID for nested location updates

    Returns:
        PushResponse with results from each receiver
    """
    receiver_responses = []
    for receiver in push.receivers:
        # get client endpoints
        if version.value.startswith("2.1") or version.value.startswith("2.0"):
            token = receiver.auth_token
        else:
            token = encode_string_base64(receiver.auth_token)

        client_auth_token = f"Token {token}"

        async with httpx.AsyncClient() as client:
            logger.info(
                f"Send request to get version details: {receiver.endpoints_url}"
            )
            response = await client.get(
                receiver.endpoints_url,
                headers={"authorization": client_auth_token},
            )
            logger.info(f"Response status_code - `{response.status_code}`")
            response_data = response.json()["data"]

            # Check if response is a versions list or VersionDetail
            # Versions list: [Version(version="2.3.0", url="..."), ...]
            # VersionDetail: VersionDetail(version="2.3.0", endpoints=[...])
            if isinstance(response_data, list):
                # It's a versions list - find the matching version and get its details
                logger.debug("Response is a versions list, finding version details URL")
                version_url = None
                for v in response_data:
                    if v.get("version") == version.value:
                        version_url = v.get("url")
                        break

                if not version_url:
                    raise ValueError(
                        f"Version {version.value} not found in versions list"
                    )

                logger.info(f"Getting version details from: {version_url}")
                details_response = await client.get(
                    version_url,
                    headers={"authorization": client_auth_token},
                )
                logger.info(
                    f"Details response status_code - `{details_response.status_code}`"
                )
                endpoints = details_response.json()["data"]["endpoints"]
            else:
                # It's a VersionDetail - extract endpoints directly
                logger.debug("Response is a VersionDetail, extracting endpoints")
                endpoints = response_data["endpoints"]

            logger.debug(f"Endpoints response data - `{endpoints}`")

        # Get object data (for PUT) or use provided partial data (for PATCH)
        if use_patch:
            if partial_data is None:
                raise ValueError("partial_data is required when use_patch=True")
            data = partial_data
            logger.debug(f"Using PATCH with partial data for module `{push.module_id}`")
        else:
            # Get full object data for PUT
            if crud is None:
                raise ValueError("crud is required when use_patch=False")
            if push.module_id == ModuleID.tokens:
                logger.debug("Requested module with push is token.")
                data = await crud.get(
                    push.module_id,
                    RoleEnum.emsp,
                    push.object_id,
                    auth_token=auth_token,
                    version=version,
                )
            else:
                logger.debug(f"Requested module with push is `{push.module_id}`.")
                data = await crud.get(
                    push.module_id,
                    RoleEnum.cpo,
                    push.object_id,
                    auth_token=auth_token,
                    version=version,
                )

        response = await send_push_request(
            push.object_id,
            data,
            push.module_id,
            adapter,
            client_auth_token,
            endpoints,
            version,
            use_patch=use_patch,
            evse_uid=evse_uid,
            connector_id=connector_id,
        )
        if push.module_id == ModuleID.cdrs:
            logger.debug("Add headers for CDR module into response.")
            receiver_responses.append(
                ReceiverResponse(
                    endpoints_url=receiver.endpoints_url,
                    status_code=response.status_code,
                    response=response.headers,
                )
            )
        else:
            receiver_responses.append(
                ReceiverResponse(
                    endpoints_url=receiver.endpoints_url,
                    status_code=response.status_code,
                    response=response.json(),
                )
            )
    result = PushResponse(receiver_responses=receiver_responses)
    logger.debug(f"Result of push operation - {result.model_dump()}")
    return result


async def push_partial_object(
    version: VersionNumber,
    push: Push,
    partial_data: dict,
    adapter: Adapter,
    auth_token: str | None = None,
    evse_uid: str | None = None,
    connector_id: str | None = None,
) -> PushResponse:
    """
    Push a partial object update using PATCH method.

    This is a convenience function for PATCH operations. It calls push_object
    with use_patch=True and the provided partial_data.

    Args:
        version: OCPI version
        push: Push request with module_id, object_id, and receivers
        partial_data: Partial update data (only changed fields + last_updated)
        adapter: Adapter to convert data (not used for PATCH, but kept for API consistency)
        auth_token: Optional auth token (not used for PATCH, but kept for API consistency)
        evse_uid: Optional EVSE UID for nested location updates
        connector_id: Optional Connector ID for nested location updates

    Returns:
        PushResponse with results from each receiver

    Example:
        ```python
        from ocpi.core.push import push_partial_object
        from ocpi.core.schemas import Push, Receiver

        push = Push(
            module_id=ModuleID.locations,
            object_id="location-123",
            receivers=[Receiver(endpoints_url="https://emsp.com/ocpi/versions", auth_token="token")]
        )

        partial_data = {
            "status": "CHARGING",
            "last_updated": "2024-01-10T12:00:00Z"
        }

        result = await push_partial_object(
            version=VersionNumber.v_2_3_0,
            push=push,
            partial_data=partial_data,
            adapter=adapter,
            evse_uid="evse-123"  # For EVSE updates
        )
        ```
    """
    return await push_object(
        version=version,
        push=push,
        crud=None,  # Not needed for PATCH
        adapter=adapter,
        auth_token=auth_token,
        use_patch=True,
        partial_data=partial_data,
        evse_uid=evse_uid,
        connector_id=connector_id,
    )


http_router = APIRouter(
    dependencies=[Depends(HttpPushVerifier())],
)


# WARNING it's advised not to expose this endpoint
@http_router.post(
    "/{version}",
    status_code=200,
    include_in_schema=False,
    response_model=PushResponse,
)
async def http_push_to_client(
    request: Request,
    version: VersionNumber,
    push: Push,
    crud: Crud = Depends(get_crud),
    adapter: Adapter = Depends(get_adapter),
):
    logger.info("Received push http request.")
    logger.debug(f"Received push data - `{push.model_dump()}`")
    auth_token = get_auth_token(request, version)

    return await push_object(version, push, crud, adapter, auth_token)


websocket_router = APIRouter(
    dependencies=[Depends(WSPushVerifier())],
)


# WARNING it's advised not to expose this endpoint
@websocket_router.websocket("/ws/{version}")
async def websocket_push_to_client(
    websocket: WebSocket,
    version: VersionNumber,
    crud: Crud = Depends(get_crud),
    adapter: Adapter = Depends(get_adapter),
):
    auth_token = get_auth_token(websocket, version)
    await websocket.accept()

    while True:
        data = await websocket.receive_json()
        logger.debug(f"Received data through ws - `{data}`")
        push = Push(**data)
        push_response = await push_object(version, push, crud, adapter, auth_token)
        logger.debug(f"Sending push response - `{push_response.model_dump()}`")
        await websocket.send_json(push_response.model_dump())
