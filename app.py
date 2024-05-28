from merrymake import Merrymake
from merrymake.merrymimetypes import MerryMimetypes
from merrymake.envelope import Envelope
from merrymake.headers import Headers

def handle_hello(payloadBytes: bytes, envelope: Envelope):
    payload = payloadBytes.decode('utf-8')
    Merrymake.reply_to_origin(f"Hello, {payload}!", Headers(MerryMimetypes.txt))

def main():
    Merrymake.service().handle("handle_hello", handle_hello)

if __name__ == "__main__":
    main()
