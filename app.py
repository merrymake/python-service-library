import sys

from merrymake import Merrymake
from merrymake.merrymimetypes import MerryMimetypes

# byte[] payloadBytes, JsonObject envelope
def handleHello(payloadBytes, envelope):
    payload = bytes(payloadBytes).decode('utf-8')
    Merrymake.reply_to_origin(f"Hello, {payload}!", MerryMimetypes.txt);

def main():
    args = sys.argv[1:]
    print(args)
    Merrymake.service(args).handle("handleHello", handleHello);

if __name__ == "__main__":
    main()
