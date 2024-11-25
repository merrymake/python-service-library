from typing import Callable, Self
from merrymake.envelope import Envelope
from merrymake.imerrymake import IMerrymake

class NullMerrymake(IMerrymake):

    def handle(self, action: str, handler: Callable[[bytes, Envelope], None]) -> Self:
        return self

    def initialize(self, f: Callable[[], None]) -> None:
        return
