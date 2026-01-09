from datetime import UTC, datetime

from pydantic import BaseModel, Field

from ocpi.core.data_types import URL, DateTime, String
from ocpi.core.enums import ModuleID


class OCPIResponse(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/2.2.1/transport_and_format.asciidoc#117-response-format
    """

    data: list | dict
    status_code: int
    status_message: String(255) | None  # type: ignore
    timestamp: DateTime = Field(  # type: ignore
        default_factory=lambda: (
            datetime.now(tz=UTC).isoformat(timespec="seconds").replace("+00:00", "Z")
        ),
    )


class Receiver(BaseModel):
    endpoints_url: URL
    auth_token: str


class Push(BaseModel):
    module_id: ModuleID
    object_id: str
    receivers: list[Receiver]


class ReceiverResponse(BaseModel):
    endpoints_url: URL
    status_code: int
    response: dict


class PushResponse(BaseModel):
    receiver_responses: list[ReceiverResponse]
