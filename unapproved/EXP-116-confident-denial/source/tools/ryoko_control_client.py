#!/usr/bin/env python3
"""Standard-library client for Ryoko's opt-in localhost rig bridge, protocol 1.

No model, speech service, credentials or automatic mutation retries are involved.
"""
from __future__ import annotations

import argparse
import json
import math
import socket
import time
from typing import Any


class BridgeError(RuntimeError):
    def __init__(self, response: dict[str, Any]):
        self.response = response
        error = response.get("error", {})
        super().__init__(f"{error.get('code', 'protocol_error')}: {error.get('message', '')}")


class RyokoClient:
    """One ordered connection. Not thread-safe; never reconnects/replays commands.

    A lost connection after a write has an uncertain outcome. Reconnect and inspect
    state; do not silently reissue the write. Each instance gets a fresh session.
    """

    WRITE_VERBS = {"apply_controls", "play_expression", "release", "reset"}
    MAX_REQUEST_BYTES = 4096
    MAX_RESPONSE_BYTES = 16384

    def __init__(self, port: int = 18163, timeout: float = 3.0):
        if type(port) is not int or not 1024 <= port <= 65535:
            raise ValueError("port must be an integer from 1024 through 65535")
        if isinstance(timeout, bool) or not math.isfinite(timeout) or timeout <= 0:
            raise ValueError("timeout must be positive and finite")
        self.socket = socket.create_connection(("127.0.0.1", port), timeout)
        self.socket.settimeout(timeout)
        self.buffer = bytearray()
        self.sequence = 0
        self.session: int | None = None
        self._last_request = 0.0
        self.last_response: dict[str, Any] = {}
        try:
            self.request("get_state")
        except BaseException:
            self.close()
            raise

    def close(self):
        self.socket.close()

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.close()

    def _read(self) -> dict[str, Any]:
        while b"\n" not in self.buffer:
            if len(self.buffer) >= self.MAX_RESPONSE_BYTES:
                raise RuntimeError("Response exceeds protocol limit")
            data = self.socket.recv(min(4096, self.MAX_RESPONSE_BYTES - len(self.buffer)))
            if not data:
                raise ConnectionError("Bridge disconnected; command outcome may be uncertain")
            self.buffer.extend(data)
        line, _, rest = self.buffer.partition(b"\n")
        self.buffer = bytearray(rest)
        return json.loads(line)

    def request(self, verb: str, args: dict[str, Any] | None = None) -> Any:
        self.sequence += 1
        request: dict[str, Any] = {"protocol": 1, "id": self.sequence, "verb": verb}
        if args is not None:
            request["args"] = args
        if verb in self.WRITE_VERBS:
            request["session"] = self.session
        data = json.dumps(request, separators=(",", ":"), allow_nan=False).encode("utf-8")
        if len(data) > self.MAX_REQUEST_BYTES:
            raise ValueError("Request exceeds protocol limit")
        # Stay below the server's sustained limit without an unbounded work queue.
        time.sleep(max(0.0, self._last_request + 1 / 30 - time.monotonic()))
        self.socket.sendall(data + b"\n")
        self._last_request = time.monotonic()
        response = self._read()
        self.last_response = response
        if response.get("protocol") != 1:
            raise RuntimeError("Unexpected response protocol")
        if response.get("id") not in (self.sequence, None) or (response.get("ok") and response.get("id") != self.sequence):
            raise RuntimeError("Unexpected response request ID")
        if not response.get("ok"):
            raise BridgeError(response)
        session = response.get("session")
        if type(session) is not int or (self.session is not None and self.session != session):
            raise RuntimeError("Unexpected connection session")
        self.session = session
        return response["result"]

    def get_state(self):
        return self.request("get_state")

    def apply_controls(self, **controls):
        return self.request("apply_controls", controls)

    def play_expression(self, expression_id: str):
        return self.request("play_expression", {"expression_id": expression_id})

    def release(self):
        return self.request("release")

    def reset(self):
        return self.request("reset")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", type=int, default=18163)
    parser.add_argument("--demo", action="store_true", help="Run the real local control demonstration")
    args = parser.parse_args()
    with RyokoClient(args.port) as client:
        def record(verb, arguments=None):
            client.request(verb, arguments)
            print(json.dumps(client.last_response, sort_keys=True), flush=True)
        record("capabilities")
        if not args.demo:
            record("get_state")
            return
        record("list_expressions")
        record("apply_controls", {"mouth_open": 0.3, "blink_R": 0.2})
        record("play_expression", {"expression_id": "EXP-163"})
        time.sleep(1.5)
        record("get_state")
        record("release")
        time.sleep(0.55)
        record("get_state")
        record("reset")


if __name__ == "__main__":
    main()
