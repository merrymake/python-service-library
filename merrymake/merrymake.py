import json
import os
import sys
import socket

from typing import Callable
from merrymake.streamhelper import read_to_end
from merrymake.nullmerrymake import NullMerrymake
from merrymake.imerrymake import IMerrymake
from merrymake.envelope import Envelope
from merrymake.headers import Headers

class Merrymake(IMerrymake):
    """Merrymake is the main class of this library, as it exposes all other
     functionality, through a builder pattern.

     @author Merrymake.eu (Chirstian Clausen, Nicolaj Græsholt)
    """

    @staticmethod
    def service():
        """This is the root call for a Merrymake service.

        Returns
        -------
        A Merrymake builder to make further calls on
        """

        args = sys.argv[1:]
        return Merrymake(args)

    def __init__(self, args):
        try:
            buffer = read_to_end(sys.stdin.buffer)
            st = 0
            actionLen = (buffer[st+0]<<16) | (buffer[st+1]<<8) | buffer[st+2]
            st += 3
            self.action = bytes(buffer[st:st+actionLen]).decode('utf-8')
            st += actionLen
            envelopeLen = buffer[st+0]<<16 | buffer[st+1]<<8 | buffer[st+2]
            st += 3
            buf = json.loads(bytes(buffer[st:st+envelopeLen]).decode('utf-8'));
            self.envelope = Envelope(buf.get("messageId"), buf.get("traceId"), buf.get("sessionId"))
            st += envelopeLen
            payloadLen = buffer[st+0]<<16 | buffer[st+1]<<8 | buffer[st+2]
            st += 3
            self.payloadBytes = bytes(buffer[st:st+payloadLen])
        except ValueError:  # includes simplejson.decoder.JSONDecodeError
            print('Decoding JSON has failed')
            raise Exception("Decoding JSON has failed")
        except:
            print("Could not read from stdin")
            raise Exception("Could not read from stdin")

    def handle(self, action: str, handler: Callable[[bytearray, Envelope], None]):
        if self.action == action:
            handler(self.payloadBytes, self.envelope)
            return NullMerrymake()
        else:
            return self

    def initialize(self, f: Callable[[], None]):
        f()

    @staticmethod
    def post_event_to_rapids(pEvent: str):
        """Post an event to the central message queue (Rapids) without a payload.

        Parameters
        ----------
        event : string
            The event to post
        """

        Merrymake.post_to_rapids(pEvent, b'')

    @staticmethod
    def post_to_rapids(pEvent: str, body: bytes | str | dict):
        """Post an event to the central message queue (Rapids) with a payload.

        Parameters
        ----------
        event : string
            The event to post
        body : string
            The payload
        """

        if pEvent == "$reply":
            body["headers"]["contentType"] = body["headers"]["content_type"].__str__()
            del body["headers"]["content_type"]
        parts = os.getenv('RAPIDS').split(":")
        with socket.socket() as s:
            s.connect((parts[0], int(parts[1])))
            byteBody = bytes(json.dumps(body), 'utf-8') if type(body) is dict else bytes(body, 'utf-8') if type(body) is str else body
            eventLen = len(pEvent)
            byteBodyLen = len(byteBody)
            s.sendall(bytes([eventLen>>16, eventLen>>8, eventLen>>0]))
            s.sendall(bytes(pEvent, 'utf-8'))
            s.sendall(bytes([byteBodyLen>>16, byteBodyLen>>8, byteBodyLen>>0]))
            s.sendall(byteBody)

    @staticmethod
    def reply_to_origin(body: str, headers: Headers):
        """Post a reply back to the originator of the trace, with a payload and its
         content type.

        Parameters
        ----------
        body : string
            The payload
        contentType : MimeType
            The content type of the payload
        """

        Merrymake.post_to_rapids("$reply", { "content": body, "headers": { "content_type": headers.contentType }})
