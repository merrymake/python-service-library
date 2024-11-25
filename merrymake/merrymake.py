import sys
from typing import Any, Callable
from merrymake.environment import Environment, RunningInMerrymake, RunningLocally
from merrymake.nullmerrymake import NullMerrymake
from merrymake.imerrymake import IMerrymake
from merrymake.envelope import Envelope
from merrymake.replypayload import ReplyPayload
from merrymake.valuemapper import Both, value_to, to

class Merrymake:
    """Merrymake is the main class of this library, as it exposes all other
     functionality, through a builder pattern.

     @author Merrymake.eu (Chirstian Clausen, Nicolaj Græsholt)
    """

    class _Merrymake(IMerrymake):
        _action: str
        _envelope: Envelope
        _payload: bytes
        def __init__(self) -> None:
            tuple = Merrymake._environment.get_input()
            self._action = tuple[0]
            self._envelope = tuple[1]
            self._payload = tuple[2]
        def handle(self, action: str, handler: Callable[[bytes, Envelope], None]) -> Any:
            if self._action == action:
                handler(self._payload, self._envelope)
                return NullMerrymake()
            else:
                return self

        def initialize(self, f: Callable[[], None]) -> None:
            f()

    _environment: Environment[Any]

    @classmethod
    def service(cls) -> IMerrymake:
        """This is the root call for a Merrymake service.

        Returns
        -------
        A Merrymake builder to make further calls on
        """

        args = sys.argv[1:]
        Merrymake._environment = RunningLocally(args) if len(args) > 0 else RunningInMerrymake()
        return Merrymake._Merrymake()

    @classmethod
    def post_to_rapids(cls, pEvent: str, body: bytes | str | dict[str,Any]) -> None:
        """Post an event to the central message queue (Rapids) with a payload.

        Parameters
        ----------
        event : string
            The event to post
        body : string
            The payload
        """

        Merrymake._environment.post(pEvent, body)

    @classmethod
    def post_event_to_rapids(cls, pEvent: str) -> None:
        """Post an event to the central message queue (Rapids) without a payload.

        Parameters
        ----------
        event : string
            The event to post
        """

        Merrymake.post_to_rapids(pEvent, b'')

    @classmethod
    def reply_to_origin(cls, reply: ReplyPayload) -> None:
        """Post a reply back to the user who triggered this trace. The payload is sent
        back using HTTP and therefore requires a content-type. For strings and json
        objects the content-type can be omitted. You can optionally supply custom
        headers and status-code if needed. Unless a status-code is supplied the
        platform always returns code "200 Ok", even if the trace has failing
        services.

        Parameters
        ----------
        reply : ReplyPayload
            content, content-type, status-code, and headers
        """

        content, c_type = value_to(
            reply["content"],
            Both(cls._environment.content_mapper, to.ContentType)
        )

        post_payload = {
            "content": {
                "type": "Buffer",
                "data": list(content)
            },
            "content-type": (
                reply["content_type"]
            ).__str__() if "content_type" in reply else str(c_type),
        }
        if "status_code" in reply:
            post_payload["status-code"] = reply["status_code"]
        if "headers" in reply:
            post_payload["headers"] = reply["headers"]

        Merrymake.post_to_rapids("$reply", post_payload)

    @classmethod
    def join_channel(cls, channel: str) -> None:
        """Subscribe to a channel
        Events will stream back messages broadcast to that channel. You can join multiple channels. You stay in the channel until the
        request is terminated.

        Note: The origin-event has to be set as "streaming: true" in the
        event-catalogue.

        Parameters
        ----------
        channel : string
            The channel to join
        """

        Merrymake.post_to_rapids("$join", channel)

    @classmethod
    def broadcast_to_channel(cls, to: str, event: str, payload: str) -> None:
        """Broadcast a message (event and payload) to all listeners in a channel.

        Parameters
        ----------
        to : string
            The channel to broadcast to
        event : string
            The event-type of the message
        payload : string
            The payload of the message
        """

        Merrymake.post_to_rapids("$broadcast", {"to": to, "event": event, "payload": payload})
