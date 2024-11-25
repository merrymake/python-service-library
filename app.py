from merrymake.envelope import Envelope
from merrymake.merrymake import Merrymake

def handle_hello(payloadBytes: bytes, envelope: Envelope) -> None:
    payload = payloadBytes.decode('utf-8')
    Merrymake.reply_to_origin({
        "content": f"Hello, {payload}!",
    })

def main() -> None:
    Merrymake.service().handle("handle_hello", handle_hello)

if __name__ == "__main__":
    main()
