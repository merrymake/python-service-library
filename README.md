# Merrymake Service Library

Service library for the Merrymake platform

## Installation

```shell
$ pip3 install merrymake
$ pip3 freeze > requirements.txt    # persist dependencies
```

## Example

A basic example that just returns `Hello, world!`,
if accessed on the platform using a payload `world`.

```python
# app.py
import sys

from merrymake import Merrymake
from merrymake.merrymimetypes import MerryMimetypes

def handleHello(payloadBytes, envelope):
    payload = bytes(payloadBytes).decode('utf-8')
    Merrymake.reply_to_origin(f"Hello, {payload}!", MerryMimetypes.txt);

def main():
    args = sys.argv[1:]
    print(args)
    Merrymake.service(args).handle("handleHello", handleHello);

if __name__ == "__main__":
    main()
```
