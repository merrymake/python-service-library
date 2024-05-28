from dataclasses import dataclass
from merrymake.merrymimetypes import MerryMimetype

@dataclass(frozen=True)
class Headers:
    contentType: MerryMimetype
