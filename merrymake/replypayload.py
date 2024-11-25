from typing import Any, TypedDict
from merrymake.contenttype import _ContentType

class ReplyPayload(TypedDict, total=False):
    status_code: int
    headers: dict[str, str]
    content: str | dict[str,Any] | None | bytes
    content_type: _ContentType
