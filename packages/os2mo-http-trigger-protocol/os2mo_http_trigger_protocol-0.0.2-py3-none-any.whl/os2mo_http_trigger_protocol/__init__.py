from uuid import UUID
from typing import Dict, List, Optional
from enum import Enum, auto, unique

from pydantic import BaseModel


class AutoNameEnum(Enum):
    def _generate_next_value_(name, start, count, last_values):
        return name


@unique
class EventType(AutoNameEnum):
    """MO Trigger EventType.

    EventType for trigger registry
    """

    ON_BEFORE = auto()
    ON_AFTER = auto()


@unique
class RequestType(AutoNameEnum):
    """MO Trigger RequestType.

    Support requests for :class:`RequestHandler`.
    """

    CREATE = auto()
    EDIT = auto()
    TERMINATE = auto()


class MOTriggerPayload(BaseModel):
    """MO trigger payload.

    See: https://os2mo.readthedocs.io/en/development/api/triggers.html#the-trigger-function for details.

    Note: data is dependent on the `event_type, `request_type` and `role_type`.
    """

    class Config:
        schema_extra = {
            "example": {
                "event_type": "ON_BEFORE",
                "request": {
                    "data": {
                        "clamp": True,
                        "name": "Havtorn Kommune",
                        "uuid": "fb2d158f-114e-5f67-8365-2c520cf10b58",
                        "validity": {"from": "2021-02-09"},
                    },
                    "type": "org_unit",
                },
                "request_type": "EDIT",
                "role_type": "org_unit",
                "uuid": "fb2d158f-114e-5f67-8365-2c520cf10b58",
            }
        }

    event_type: EventType
    request: Dict
    request_type: RequestType
    role_type: str
    uuid: UUID


class MOTriggerRegister(BaseModel):
    """Return value for /triggers.

    Contains the information that MO needs to register the trigger.
    """

    class Config:
        schema_extra = {
            "example": {
                "event_type": 0,
                "request_type": 0,
                "role_type": "org_unit",
                "url": "/triggers/ou/create",
                "timeout": 60,
            }
        }

    event_type: EventType
    request_type: RequestType
    role_type: str
    url: str
    timeout: Optional[int]
