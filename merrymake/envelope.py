from dataclasses import dataclass
from typing import TypedDict, Optional

@dataclass(frozen=True)
class Envelope(TypedDict):
    message_id: str
    """
    Id of this particular message.
    Note: it is _not_ unique, since multiple rivers can deliver the same message.
    The combination of (river, messageId) is unique.
    """

    trace_id: str
    """
    Id shared by all messages in the current trace, ie. stemming from the same
    origin.
    """

    session_id: Optional[str]
    """
    (Optional) Id corresponding to a specific originator. This id is rotated occasionally,
    but in the short term it is unique and consistent. Same sessionId implies
    the trace originated from the same device.
    """

    headers: Optional[dict[str, str]]
    """
    (Optional) If this is the first service in the trace, this will hold any unusual HTTP headers from the triggering HTTP call.

    _Note_: Always lowercase.
    """