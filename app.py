import sys

from merrymake import Merrymake
from merrymake.merrymimetypes import MerryMimetypes
from merrymake.envelope import Envelope

def handleHello(payloadBytes: bytearray, envelope: Envelope):
    payload = bytes(payloadBytes).decode('utf-8')
    Merrymake.reply_to_origin(f"Hello, {payload}!", MerryMimetypes.getMimeType("txt"));

def main():
    Merrymake.service().handle("handleHello", handleHello);

if __name__ == "__main__":
    main()
