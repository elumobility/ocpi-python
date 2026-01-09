
from pydantic import BaseModel

from ocpi.core.data_types import URL, CiString, DateTime, DisplayText
from ocpi.modules.commands.v_2_3_0.enums import (
    CommandResponseType,
    CommandResultType,
)
from ocpi.modules.tokens.v_2_3_0.schemas import Token


class CancelReservation(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/2.3.0/mod_commands.asciidoc#131-cancelreservation-object
    """

    response_url: URL
    reservation_id: CiString(36)  # type: ignore


class CommandResponse(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/2.3.0/mod_commands.asciidoc#132-commandresponse-object
    """

    result: CommandResponseType
    timeout: int
    message: list[DisplayText] = []


class CommandResult(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/2.3.0/mod_commands.asciidoc#133-commandresult-object
    """

    result: CommandResultType
    message: list[DisplayText] = []


class ReserveNow(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/2.3.0/mod_commands.asciidoc#134-reservenow-object
    """

    response_url: URL
    token: Token
    expiry_date: DateTime
    reservation_id: CiString(36)  # type: ignore
    location_id: CiString(36)  # type: ignore
    evse_uid: CiString(36) | None  # type: ignore
    authorization_reference: CiString(36) | None  # type: ignore


class StartSession(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/2.3.0/mod_commands.asciidoc#135-startsession-object
    """

    response_url: URL
    token: Token
    location_id: CiString(36)  # type: ignore
    evse_uid: CiString(36) | None  # type: ignore
    connector_id: CiString(36) | None  # type: ignore
    authorization_reference: CiString(36) | None  # type: ignore


class StopSession(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/2.3.0/mod_commands.asciidoc#136-stopsession-object
    """

    response_url: URL
    session_id: CiString(36)  # type: ignore


class UnlockConnector(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/2.3.0/mod_commands.asciidoc#137-unlockconnector-object
    """

    response_url: URL
    location_id: CiString(36)  # type: ignore
    evse_uid: CiString(36)  # type: ignore
    connector_id: CiString(36)  # type: ignore
