#!/usr/bin/env python3
"""Real subprocess/socket tests. Uses the actual viewer and controller, not mocks."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import socket
import subprocess
import tempfile
import time

from ryoko_control_client import RyokoClient, BridgeError

ROOT = Path(__file__).resolve().parents[1]


class Wire:
    def __init__(self, port):
        self.socket = socket.create_connection(("127.0.0.1", port), 3)
        self.socket.settimeout(4)
        self.buffer = bytearray()
        self.sequence = 0
        self.session = None

    def close(self):
        self.socket.close()
        time.sleep(0.04)

    def send(self, data):
        self.socket.sendall(data)

    def read(self):
        while b"\n" not in self.buffer:
            data = self.socket.recv(16384)
            if not data:
                raise EOFError("closed")
            self.buffer.extend(data)
        line, _, self.buffer = self.buffer.partition(b"\n")
        return json.loads(line)

    def request(self, verb="get_state", args=None, **extra):
        time.sleep(0.02)
        self.sequence += 1
        item = {"protocol": 1, "id": self.sequence, "verb": verb}
        if args is not None:
            item["args"] = args
        if verb in RyokoClient.WRITE_VERBS:
            item["session"] = self.session
        item.update(extra)
        self.send(json.dumps(item, separators=(",", ":")).encode() + b"\n")
        response = self.read()
        if self.session is None:
            self.session = response.get("session")
        return response


class Suite:
    def __init__(self, output, godot):
        self.output = output
        self.output.mkdir(parents=True, exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(prefix="ryoko-bridge-")
        self.directory = Path(self.temp.name)
        self.sequence = 0
        self.checks = []
        self.godot = godot
        self.process = None
        self.wire = None
        with socket.socket() as probe:
            probe.bind(("127.0.0.1", 0))
            self.port = probe.getsockname()[1]
        self.env = os.environ.copy()
        for key, name in [("HOME", "home"), ("XDG_CACHE_HOME", "cache"), ("XDG_DATA_HOME", "data"), ("XDG_CONFIG_HOME", "config")]:
            path = self.directory / name
            path.mkdir()
            self.env[key] = str(path)

    def check(self, condition, label):
        if not condition:
            raise AssertionError(label)
        self.checks.append(label)

    def command(self, action="snapshot", **fields):
        self.sequence += 1
        path = self.directory / "command.tmp"
        path.write_text(json.dumps({"sequence": self.sequence, "action": action, **fields}))
        path.replace(self.directory / "command.json")
        deadline = time.monotonic() + 5
        while time.monotonic() < deadline:
            try:
                reply = json.loads((self.directory / "reply.json").read_text())
                if reply.get("sequence") == self.sequence:
                    return reply
            except (FileNotFoundError, json.JSONDecodeError):
                pass
            time.sleep(.01)
        raise TimeoutError("test host command " + action)

    def connect(self):
        if self.wire:
            self.wire.close()
        self.wire = Wire(self.port)
        self.check(self.wire.request()["ok"], "new connection state read")
        return self.wire

    def reject(self, verb, args, code="invalid_controls", **fields):
        before = self.command()["snapshot"]
        response = self.wire.request(verb, args, **fields)
        self.check(not response["ok"] and response["error"]["code"] == code, f"reject {verb} {args!r} {fields!r}")
        self.check(self.command()["snapshot"] == before, "invalid command preserves pose/clock/owner/internal state")

    def raw_reject(self, data, code="invalid_json"):
        before = self.command()["snapshot"]
        self.wire.send(data + b"\n")
        response = self.wire.read()
        self.check(not response["ok"] and response["error"]["code"] == code, "reject malformed " + repr(data[:100]))
        self.check(self.command()["snapshot"] == before, "malformed input is atomic")

    def run(self):
        log = (self.output / "godot_bridge.log").open("w")
        self.process = subprocess.Popen([self.godot, "--headless", "--path", str(ROOT), "--script", "res://tests/control_bridge_host.gd", "--", f"--control-port={self.port}", f"--test-directory={self.directory}"], stdout=log, stderr=subprocess.STDOUT, env=self.env)
        deadline = time.monotonic() + 10
        while not (self.directory / "reply.json").exists() and time.monotonic() < deadline:
            if self.process.poll() is not None:
                raise RuntimeError("Godot exited during startup")
            time.sleep(.03)
        self.check((self.directory / "reply.json").exists(), "real Godot viewer ready")
        # Default and invalid startup never enable a listener. A conflicting bind
        # must fail without disturbing the live primary process.
        for arguments, expected in [([], None), (["--control-port=abc"], "must be an integer"), (["--control-port=0"], "Port must be"), ([f"--control-port={self.port}", "--control-port=18164"], "only once"), ([f"--control-port={self.port}"], "Cannot bind loopback")]:
            result = subprocess.run([self.godot, "--headless", "--path", str(ROOT), "--quit-after", "4", "--", *arguments], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, env=self.env, timeout=10)
            self.check(result.returncode == 0 and "SCRIPT ERROR" not in result.stdout, "viewer startup remains usable " + repr(arguments))
            if expected:
                self.check(expected in result.stdout, "explicit startup error " + expected)
        # Merely guessing a session cannot bypass the discovery handshake.
        self.wire = Wire(self.port)
        response = self.wire.request("reset", {}, session=1)
        self.check(response["error"]["code"] == "stale_session", "discovery required before writes")
        w = self.connect()
        caps = w.request("capabilities")["result"]
        self.check(caps["expressions"] == [{"id": "EXP-163", "title": "Yawn", "duration": 5.8, "aliases": ["yawn"]}, {"id": "EXP-005", "title": "Hearty laughter", "duration": 5.4, "aliases": ["hearty-laughter", "laugh"]}, {"id": "EXP-001", "title": "Bright welcome", "duration": 3.0, "aliases": ["bright_welcome"]}, {"id": "EXP-006", "title": "Suppressed giggle", "duration": 2.8, "aliases": ["suppressed-giggle", "giggle"]}], "only authored shared performances exposed")
        self.check(caps["physical_mouth_max"] == .55 and not caps["ai_model_connected"] and not caps["tts_connected"], "honest bounds and integration scope")
        self.check(len(w.request("list_expressions")["result"]) == 4, "external enumeration")
        for channel in ["mouth_smile", "mouth_spread", "mouth_corner_lift", "mouth_lip_press", "blush_intensity", "eye_smile_R", "eye_smile_L"]:
            self.check(caps["controls"][channel] == [0.0, 1.0], "advertised bounded smile " + channel)
            self.check(w.request("apply_controls", {channel: .375})["ok"], "socket accepts smile " + channel)
            self.check(self.command()["snapshot"]["controls"][channel] == .375, "socket applies shared smile owner " + channel)
            for invalid in [-.000001, 1.000001, True, "0"]:
                self.reject("apply_controls", {channel: invalid, "reset": True})
        self.check(w.request("play_expression", {"expression_id": "laugh"})["ok"], "socket triggers shared laughter alias")
        self.command("advance", value=1.30)
        self.check(self.command()["snapshot"]["controls"]["mouth_smile"] > .9, "socket laughter reaches articulated smile")
        w.request("reset")
        expected_gaze = [-1.0, 1.0] if caps["gaze"]["enabled"] else [0.0, 0.0]
        self.check(caps["controls"]["gaze_x"] == expected_gaze and caps["controls"]["gaze_y"] == expected_gaze, "advertised gaze switch and units")
        calibration = caps["gaze"]["calibration"]
        self.check(calibration == {"status": "verified_enabled" if caps["gaze"]["enabled"] else "coverage_bounded_pending_visual_qa", "left": 4.0, "right": 4.0, "up": 2.0, "down": 1.0}, "calibration records narrowed down travel and QA status")
        self.check(all(caps["gaze"][direction] == (calibration[direction] if caps["gaze"]["enabled"] else 0.0) for direction in ["left", "right", "up", "down"]), "active physical support is zero while disabled")
        for x in expected_gaze:
            for y in expected_gaze:
                self.check(w.request("apply_controls", {"gaze_x": x, "gaze_y": y})["ok"], "advertised gaze corner accepted")
        for value in [expected_gaze[0] - .000001, expected_gaze[1] + .000001, True, "0"]:
            self.reject("apply_controls", {"gaze_y": value, "mouth_open": .2, "reset": True})
        w.request("reset")
        self.check(w.request("apply_controls", {"mouth_open": .3, "blink_R": .2})["ok"], "external manual controls")
        self.check(self.command()["snapshot"]["controls"]["mouth_open"] == .3, "socket changes actual shared rig")
        self.check(w.request("play_expression", {"expression_id": "yawn"})["ok"], "external trigger via alias")
        self.command("advance", value=1.7)
        playing = self.command()["snapshot"]
        self.check(playing["active_expression"] == "EXP-163" and playing["owners"]["mouth"] == "EXP-163", "actual controller expression ownership")

        # Frozen clocks make invalid-transaction atomicity observable exactly.
        for mode in ["performance", "release", "manual", "neutral"]:
            if mode == "release":
                self.check(w.request("release")["ok"], "external release")
                self.command("advance", value=.1)
            elif mode == "manual":
                w.request("apply_controls", {"mouth_open": .42})
            elif mode == "neutral":
                w.request("reset")
            for controls in [{"mouth_open": True}, {"mouth_open": "0.3"}, {"mouth_open": -0.01}, {"mouth_open": 1.01}, {"hair_sway": .070001}, {"gaze_x": caps["controls"]["gaze_x"][1] + .001}, {"viseme": "A"}, {"mouth": "O"}, {"reset": True, "unknown": 1}, {"auto_blink": 1}, {"blink": False}, {"perform_expression": "EXP-007"}, {"mouth_open": .3, "mouth": "REST"}, {"release_performance": True, "blink": .3}, {"perform_expression": "EXP-163", "reset": True}]:
                self.reject("apply_controls", controls)
            self.reject("play_expression", {"expression_id": "res://object_rig.gd"})
            self.reject("play_expression", {"expression_id": True}, "invalid_args")
            self.reject("reset", {"extra": 1}, "invalid_args")
            self.reject("advance", {}, "unknown_verb")
            self.reject("apply_controls", [], "invalid_args")
            self.reject("reset", {}, "unknown_field", path="res://object_rig.gd")
            self.reject("reset", {}, "stale_session", session=True)
            self.reject("reset", {}, "stale_session", session=w.session + 1)
            self.reject("get_state", {}, "unsupported_protocol", protocol=True)

        for data in [b"", b"not json", b"{} trailing", b'{"protocol":1,}', b'{"protocol":1,"protocol":1}', b'{"x":1,"\\u0078":2}', b'{"x":NaN}', b'{"x":Infinity}', b'{"x":1e999}', b'{"x":01}', b'{"x":.1}', b'{"x":1.}', b'{"x":"\\q"}', b'{"x":"\xff"}', b'{"x":' + b'[' * 9 + b'0' + b']' * 9 + b'}', b'[' + b'0,' * 256 + b'0]']:
            self.raw_reject(data)
        self.raw_reject(b'[]', "invalid_request")
        for bad_id in [None, True, False, 0, -1, 1.5, 2147483648, "7"]:
            self.raw_reject(json.dumps({"protocol": 1, "id": bad_id, "verb": "reset"}).encode(), "invalid_id")

        # Exact size boundary, fragmented TCP, CRLF and pipelined requests.
        w.sequence += 1
        item = json.dumps({"protocol": 1, "id": w.sequence, "verb": "get_state"}).encode()
        line = item + b" " * (4096 - len(item))
        for part in [line[:1], line[1:19], line[19:-1], line[-1:], b"\n"]:
            w.send(part); time.sleep(.02)
        self.check(w.read()["ok"], "fragmented 4096-byte boundary accepted")
        w.sequence += 1
        w.send(json.dumps({"protocol": 1, "id": w.sequence, "verb": "get_state"}).encode() + b"\r\n")
        self.check(w.read()["ok"], "CRLF framing accepted")
        requests = [{"protocol": 1, "id": w.sequence + i, "verb": "get_state"} for i in range(1, 5)]
        w.sequence += 4
        w.send(b"".join(json.dumps(x).encode() + b"\n" for x in requests))
        self.check([w.read()["id"] for _ in requests] == [x["id"] for x in requests], "pipelined acknowledgments ordered")
        self.reject("reset", {}, "stale_id", id=w.sequence)
        self.reject("reset", {}, "stale_id", id=1)

        # Retry must not restart a performance.
        w.request("play_expression", {"expression_id": "EXP-163"})
        previous_id = w.sequence
        self.command("advance", value=1.0)
        self.reject("play_expression", {"expression_id": "EXP-163"}, "stale_id", id=previous_id)
        self.check(w.request("play_expression", {"expression_id": "EXP-163"})["result"]["rig"]["time"] == 0, "new ID explicitly retriggers")
        self.command("advance", value=1.3)
        self.check(w.request("release")["result"]["rig"]["owners"]["mouth"] == "release", "release acknowledged immediately")
        self.command("advance", value=.45)
        self.check(w.request()["result"]["rig"]["controls"]["mouth_open"] == 0, "release reaches neutral")
        w.request("apply_controls", {"mouth_open": 1.0, "hair_sway": -.07})
        old_session = w.session
        before = self.command()["snapshot"]
        w = self.connect()
        self.check(self.command()["snapshot"] == before, "disconnect/reconnect retains controller without hidden pose mutation")
        self.reject("reset", {}, "stale_session", session=old_session)
        self.check(w.request("reset")["ok"], "fresh session explicitly resets")
        self.check(self.command()["snapshot"]["controls"]["mouth_open"] == 0, "reset neutral")

        # Secondary client rejected, and it cannot steal existing control.
        second = Wire(self.port)
        try:
            busy = second.read()
            self.check(busy["error"]["code"] == "busy", "second connection rejected")
        finally:
            second.close()
        self.check(w.request()["ok"], "original connection retained")

        self.command("manual_invalid")
        self.check(w.request()["result"]["bridge"]["external_enabled"], "invalid UI command does not revoke external control")
        self.command("manual_slider", value=.321)
        try:
            w.read()
            raise AssertionError("manual takeover should close old connection")
        except (EOFError, ConnectionResetError):
            self.check(True, "manual slider discards old connection")
        w = self.connect()
        self.reject("apply_controls", {"mouth_open": .9}, "manual_lock")
        self.check(abs(self.command()["snapshot"]["controls"]["mouth_open"] - .321) < 1e-6, "manual pose survives reconnect")
        self.command("enable")
        w = self.connect()
        self.check(w.request("apply_controls", {"mouth_open": .2})["ok"], "UI re-enable permits fresh external session")
        # Queue many commands then invoke the real UI signal. Whatever arrived first,
        # no old request can execute after the local takeover is acknowledged.
        w.send(b"".join(json.dumps({"protocol": 1, "id": w.sequence + i, "verb": "apply_controls", "session": w.session, "args": {"mouth_open": .9}}).encode() + b"\n" for i in range(1, 17)))
        self.command("manual_slider", value=.432)
        time.sleep(.2)
        self.check(abs(self.command()["snapshot"]["controls"]["mouth_open"] - .432) < 1e-6, "stale queued actions cannot override UI takeover")
        self.command("enable");w = self.connect()
        for key in [80, 32, 48]:
            self.command("key", value=key)
            self.check(not self.command()["bridge"]["external_enabled"], "keyboard action revokes external control")
            self.command("enable");w = self.connect()

        # Oversize and stalled fragments close explicitly, without changing the rig.
        before = self.command()["snapshot"]
        w.send(b" " * 4097)
        self.check(w.read()["error"]["code"] == "message_too_large", "oversized incomplete line rejected")
        self.check(self.command()["snapshot"] == before, "oversize rejection atomic")
        w = self.connect()
        w.send(b'{"protocol":')
        self.check(w.read()["error"]["code"] == "partial_timeout", "stalled fragment deadline enforced")
        self.check(self.command()["snapshot"] == before, "partial timeout atomic")
        w = self.connect()
        # Saturate at 100 requests in one batch: bounded work and explicit rate error.
        w.send(b"".join(json.dumps({"protocol": 1, "id": 100 + i, "verb": "get_state"}).encode() + b"\n" for i in range(100)))
        responses = []
        while True:
            try:
                responses.append(w.read())
            except (EOFError, ConnectionResetError):
                break
        self.check(any(x.get("error", {}).get("code") == "rate_limited" for x in responses), "request flood bounded and rejected")
        self.check(len(responses) < 100, "rate limit prevents executing full flood")
        self.check(self.command()["snapshot"] == before, "rate failure preserves pose")
        w.close(); self.wire = None
        with RyokoClient(self.port) as client:
            self.check(client.request("capabilities")["name"] == "ryoko-shared-rig-control", "standard-library client handshake")
            client.play_expression("EXP-163")
            self.command("run_clock", value=True)
            time.sleep(.2)
            self.check(client.get_state()["rig"]["time"] > .05, "live Godot process advances expression")
            client.release(); time.sleep(.55)
            self.check(client.get_state()["rig"]["controls"]["mouth_open"] == 0, "live Godot release completes")
            client.reset()
            try:
                client.apply_controls(mouth_open=True)
            except BridgeError as error:
                self.check(error.response["error"]["code"] == "invalid_controls", "client reports explicit error")
        time.sleep(.05)
        self.command("run_clock", value=False)
        # An idle client cannot hold the single slot forever. No hidden release.
        w = self.connect()
        before_idle = self.command()["snapshot"]
        w.socket.settimeout(33)
        idle = w.read()
        self.check(idle["error"]["code"] == "idle_timeout", "idle connection deadline enforced")
        self.check(self.command()["snapshot"] == before_idle, "idle timeout does not mutate pose or clock")
        self.command("stop")
        with socket.socket() as probe:
            self.check(probe.connect_ex(("127.0.0.1", self.port)) != 0, "stop closes listening socket")
        self.command("quit")
        self.check(self.process.wait(timeout=5) == 0, "clean Godot shutdown")
        log.close()
        self.check("SCRIPT ERROR" not in (self.output / "godot_bridge.log").read_text(), "no script errors in actual host")
        report = {"status": "PASS", "checks": len(self.checks), "real_process": True, "godot": subprocess.check_output([self.godot, "--version"], text=True, env=self.env).strip(), "coverage": self.checks}
        (self.output / "control_bridge_results.json").write_text(json.dumps(report, indent=2) + "\n")
        print(f"CONTROL_BRIDGE_PASS checks={len(self.checks)} real_process=true")

    def close(self):
        if self.wire:
            self.wire.close()
        if self.process and self.process.poll() is None:
            self.process.terminate()
            self.process.wait(timeout=5)
        self.temp.cleanup()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True, help="Evidence directory outside source")
    parser.add_argument("--godot", default="godot")
    args = parser.parse_args()
    suite = Suite(args.output.resolve(), args.godot)
    try:
        suite.run()
    finally:
        suite.close()


if __name__ == "__main__":
    main()
