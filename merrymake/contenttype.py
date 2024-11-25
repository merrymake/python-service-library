from typing import Final

class _ContentType:
    _kind: str
    _name: str
    def __init__(self, kind: str, name: str) -> None:
        self._kind = kind
        self._name = name

    def __str__(self) -> str:
        return f"{self._kind}/{self._name}"
class ContentType (_ContentType):
    # Images
    gif: Final[_ContentType] = _ContentType("image", "gif")
    jpeg: Final[_ContentType] = _ContentType("image", "jpeg")
    png: Final[_ContentType] = _ContentType("image", "png")
    svg: Final[_ContentType] = _ContentType("image", "svg+xml")
    webp: Final[_ContentType] = _ContentType("image", "webp")
    # Strings
    csv: Final[_ContentType] = _ContentType("text", "csv")
    html: Final[_ContentType] = _ContentType("text", "html")
    json: Final[_ContentType] = _ContentType("application", "json")
    text: Final[_ContentType] = _ContentType("text", "plain")
    xml: Final[_ContentType] = _ContentType("application", "xml")
    # Unknown
    raw: Final[_ContentType] = _ContentType("application", "octet-stream")
