import json

class Envelope:
    def __init__(self, arg: str):
        buf = json.loads(arg);
        self.messageId = buf.get("messageId");
        self.traceId = buf.get("traceId");
        self.sessionId = buf.get("sessionId");
