from abc import ABC, abstractmethod
import json
import os
import socket
import sys
from typing import Any, Generic, TypeVar
from merrymake.envelope import Envelope
from merrymake.streamhelper import read_to_end
from merrymake.valuemapper import ValueMapper, to, value_to

T = TypeVar('T')

class Environment(Generic[T],ABC):
    @property
    @abstractmethod
    def content_mapper(self) -> ValueMapper[T]:
        pass
    @abstractmethod
    def get_input(self) -> tuple[str, Envelope, bytes]:
        pass
    @abstractmethod
    def post(self,
        event: str,
        payload: None | bytes | str | dict[str,Any]
    ) -> None:
        pass

class RunningLocally(Environment[str]):
    _args: list[str]
    _content_mapper = to.String
    @property
    def content_mapper(self) -> ValueMapper[str]:
        return self._content_mapper
    def __init__(self, args: list[str]) -> None:
        self._args = args
    def get_input(self) -> tuple[str, Envelope, bytes]:
        if len(self._args) > 2:
            buf = json.loads(self._args[2])
            envelope = Envelope(
                message_id=buf.get("messageId"),
                trace_id=buf.get("traceId"),
                session_id=buf.get("sessionId"),
                headers=buf.get("headers")
            )
        else:
            envelope = None
        return (
            self._args[0],
            envelope,
            bytes(self._args[1], 'utf-8') if len(self._args) > 1 else bytes(),
        )
    def post(self,
        event: str,
        payload: None | bytes | str | dict[str,Any]
    ) -> None:
        print(f"{event}: {value_to(payload, to.String)}")

class RunningInMerrymake(Environment[bytes]):
    _content_mapper = to.Bytes
    @property
    def content_mapper(self) -> ValueMapper[bytes]:
        return self._content_mapper
    def get_input(self) -> tuple[str, Envelope, bytes]:
        try:
            buffer = read_to_end(sys.stdin.buffer)
            st = 0
            actionLen = (buffer[st+0]<<16) | (buffer[st+1]<<8) | buffer[st+2]
            st += 3
            action = bytes(buffer[st:st+actionLen]).decode('utf-8')
            st += actionLen
            envelopeLen = buffer[st+0]<<16 | buffer[st+1]<<8 | buffer[st+2]
            st += 3
            buf = json.loads(bytes(buffer[st:st+envelopeLen]).decode('utf-8'))
            envelope = Envelope(
                message_id=buf.get("messageId"),
                trace_id=buf.get("traceId"),
                session_id=buf.get("sessionId"),
                headers=buf.get("headers")
            )
            st += envelopeLen
            payloadLen = buffer[st+0]<<16 | buffer[st+1]<<8 | buffer[st+2]
            st += 3
            payloadBytes = bytes(buffer[st:st+payloadLen])
            return (action, envelope, payloadBytes)
        except ValueError:  # includes simplejson.decoder.JSONDecodeError
            print('Decoding JSON has failed')
            raise Exception("Decoding JSON has failed")
        except:
            print("Could not read from stdin")
            raise Exception("Could not read from stdin")
    def post(self,
        event: str,
        payload: None | bytes | str | dict[str,Any]
    ) -> None:
        rapids = os.getenv('RAPIDS')
        assert rapids is not None, "RAPIDS should not be None"
        parts = rapids.split(":")
        with socket.socket() as s:
            s.connect((parts[0], int(parts[1])))
            byteBody = bytearray(value_to(payload, to.Bytes))
            eventLen = len(event)
            byteBodyLen = len(byteBody)
            s.sendall(bytearray([(eventLen>>16)&255, (eventLen>>8)&255, (eventLen>>0)&255]))
            s.sendall(bytearray(bytes(event, 'utf-8')))
            s.sendall(bytearray([(byteBodyLen>>16)&255, (byteBodyLen>>8)&255, (byteBodyLen>>0)&255]))
            s.sendall(byteBody)
