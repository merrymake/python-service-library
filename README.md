# Python Service Library for Merrymake

This is the official Python service library for [Merrymake](https://www.merrymake.eu). It defines all the basic functions needed to work with Merrymake.

## Usage

Here is the most basic example of how to use this library:

```python
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
```

## Tutorials and templates

For more information check out our tutorials at [merrymake.dev](https://merrymake.dev).

All templates are available through our CLI and on our [GitHub](https://github.com/merrymake).
