# Local external-process control, protocol 1

This is a **real local TCP connection to the default viewer's single shared Godot
rig**. The included Python client runs in another process and receives actual
controller results. No AI model, Ryoko agent service, voice/TTS provider or
lip-sync service is connected. No credentials or persistent authorization are
created. Only EXP-163 / Yawn is authored.

## Run a reproducible demonstration

From this project, with Godot 4.6.3 and Python 3:

```sh
godot --headless --path . --editor --quit
godot --path . -- --control-port=18163
```

In another terminal:

```sh
python tools/ryoko_control_client.py --port 18163 --demo
```

The client discovers capabilities and the catalogue, sets bounded manual values,
plays the approved yawn, reads its advancing state, releases it, observes the
neutral return, then resets. Every printed JSON line is a real server response.
Omit `--demo` for read-only discovery/state. Use `godot --headless --path . --
--control-port=18163` for a non-visual service with the identical default scene.
Terminate that process to stop the listener; there is no remote shutdown verb.
On a restricted executor, set HOME and XDG cache/config/data directories to
writable temporary directories before starting Godot.

A normal launch without `--control-port` creates **no listener**. The one optional
port must be an integer in 1024..65535 and must be free. Duplicate arguments,
invalid ports and bind failures are reported in the viewer and Godot log; the
viewer remains usable without the bridge. Binding is hard-coded to IPv4
`127.0.0.1`; there is no host override, internet listener, discovery broadcast,
remote-machine execution or automatic service startup.

## Security and integration boundary

The listener trusts processes already running on this computer. Loopback is not
an authentication boundary against malicious local users/processes. Do not
forward this port, expose it through a proxy, or run it on an untrusted shared
machine. There are no auth tokens to mistake for internet-facing security.

`control_bridge.gd` receives the viewer's existing `rig` reference. Its seven
allowlisted verbs either read public state/catalogue or call that rig's existing
`apply_controls` validator. It does not instantiate another rig, use a second
animation clock, evaluate code, dispatch arbitrary method names, accept resource
paths, register expression data, read/write files, or call the historical
lower-level viseme API. The server cannot advance/seek the clock remotely.

The nearby Ryoko gateway's `gateway/control_socket.py` was inspected read-only.
It uses versioned JSON verbs over a separate ACL-protected Unix socket/Windows
pipe for gateway coordination; it provides no found VTuber-control adapter.
This bridge reuses the JSON `protocol`/`verb` convention, not that gateway's
privileged service or identity. Native Godot TCP and Python's standard library
provide a small cross-platform local adapter. No changes to that repository or
communication with its agents were made. A future approved AI adapter can import
`RyokoClient`, discover capabilities and submit these bounded transactions.

## Wire contract

One UTF-8 JSON object per newline, on one persistent TCP connection. CRLF is
accepted. Fragmented reads and multiple complete lines are supported. Strict
JSON rejects trailing commas, duplicate keys (including escaped duplicates),
invalid UTF-8, nonfinite numbers, excessive nesting and excessive values.

Request fields:

- `protocol`: numeric integer 1, never boolean or a string.
- `id`: numeric integer 1..2147483647, strictly increasing on this connection.
  Gaps are allowed; equality/backtracking is an error. Valid IDs are consumed
  even if a later schema/control check fails. Malformed JSON or invalid IDs do
  not consume an ID.
- `verb`: one of the seven strings below.
- `args`: optional object, default `{}`. No unused fields are accepted.
- `session`: required only for a mutating verb. First obtain it from a successful
  `get_state` or `capabilities` response on this connection. The positive counter
  identifies this live connection, not a credential. It changes on reconnect
  within this process and resets when the process restarts. Discovery is required
  even if a counter is guessed. Never copy a session from an earlier connection.

Read verbs:

- `capabilities`: bounds, commands, expression catalogue, transport limits and
  current bridge status. Takes no arguments.
- `list_expressions`: the shared registry's detached catalogue. No arguments.
- `get_state`: `{rig: <shared controller state>, bridge: <transport status>}`.
  No arguments.

Mutating verbs:

- `apply_controls`: `args` is exactly the shared API's control dictionary.
- `play_expression`: `args` must be exactly `{"expression_id":"EXP-163"}` or
  another actually registered ID/alias.
- `release`: no arguments; performs the existing smooth 0.45-second release.
- `reset`: no arguments; performs the existing immediate neutral reset.

Example discovery and response (response shortened only in this document):

```json
{"protocol":1,"id":1,"verb":"get_state"}
{"protocol":1,"id":1,"session":1,"ok":true,"result":{"rig":{},"bridge":{}}}
```

Then a trigger:

```json
{"protocol":1,"id":2,"session":1,"verb":"play_expression","args":{"expression_id":"EXP-163"}}
```

Acknowledgments echo `protocol`, `id` and `session`, set `ok:true`, and include a
`result`. Mutating results include the actual rig state immediately after the
transaction, not a prediction or the final animation state. The live Godot clock
continues on subsequent frames. Errors set `ok:false` and include
`error:{code,message}`. `id:null` is used when no valid ID can safely be identified
or for connection-level errors. Busy rejection is a best-effort bounded error
followed by closure. There are no unsolicited pose events; poll `get_state`.

An invalid request never changes pose, animation clock or feature ownership.
The shared controller may update its diagnostic `last_error`; transport ID/rate
bookkeeping can also change. In a running viewer, time can advance naturally
between separate reads. Tests freeze the existing controller clock to compare
complete internal snapshots exactly across invalid transactions.

See `CONTROL_API.md` for transaction combinations, no-ops and channel semantics.
Mouth remains normalized 0..1 mapped to physical 0..0.55, hair is ±0.07, local candidate gaze is normalized±1 with calibrated left/right4px, up2px/down1px, and
A/E/I/O/U visemes remain rejected. `capabilities.controls.gaze_x/gaze_y` always
report active bounds. `capabilities.gaze` reports enabled status, normalized input
units, and active source-pixel travel (all four directional fields are zero
while disabled). Its `calibration` object separately records coverage-bounded
left/right 4 px, up 2 px, down 1 px with status
`coverage_bounded_pending_visual_qa` while disabled, or `verified_enabled` after
activation. Calibration does not imply active support. Enabling permits
normalized [-1,1] only after both eyes and all corners
and eyelid combinations are verified. Positive x is right; positive y is down.

## Manual takeover, disconnect and retry

- A successful non-no-op viewer control, slider, checkbox, Play/Release/Reset
  button or P/Space/0 shortcut takes immediate precedence. The existing
  controller handles the pose. The bridge disables external writes and closes
  the current connection, discarding all received/queued messages and replies.
- While locked, a new connection can read capabilities/state but every write
  returns `manual_lock`. Reconnecting alone cannot override the person.
- Press **Enable external control** in the viewer to permit writes again. This
  also closes any reading connection. Reconnect, discover the new session, then
  send new commands. No old queue is resumed. There is no remote unlock verb.
- Invalid UI commands and the shared empty/false-reset/false-release no-ops do
  not take ownership or lock external control.
- A network disconnect, timeout, malformed request, overload or bridge stop
  discards transport buffers but performs **no hidden pose command**. An active
  approved expression/release continues on the existing clock; a static manual
  pose remains. This ensures a rejected request cannot indirectly reset/release
  the rig. Use an explicit release/reset or local UI to change it.
- Duplicate/older request IDs return `stale_id`; they never execute again.
  A new ID is a new command, so an intentional new play can retrigger.
- If the connection drops before an acknowledgment arrives, execution is
  **uncertain**. The client never reconnects/retries mutations automatically.
  Reconnect and read state first. There is no durable exactly-once history across
  connections or process restarts; do not replay an old command stream.

Feature owners remain the existing controller's expression ID, `release` or
`manual`; the transport does not invent per-channel owners. `external_enabled`
is permission to submit a transaction, not a second animation/ownership system.

## Resource bounds

- One active client. A second connection cannot steal it.
- Maximum message: 4096 bytes before newline. The application input buffer is
  at most 4097 bytes; no unbounded decoded command queue exists.
- Strict JSON depth at most 8 and at most 256 values.
- At most four complete requests per frame, token bucket 60 requests/second,
  burst capacity 20. Read requests and errors count too. The example client
  limits itself to 30 requests/second and has no background queue.
- Maximum response 16384 bytes, application output queue at most 32768 bytes.
  Full response capacity is reserved before executing a transaction. Reads stop
  under output pressure. An unsendable response/peer disconnect can still leave
  a mutation's delivery uncertain, as with any stream connection.
- Partial-message timeout 2 seconds, blocked-output timeout 2 seconds, idle
  timeout 30 seconds without a complete request. Size/rate/timeouts report an
  error when delivery is possible, then close. Invalid complete messages receive
  an error and leave the connection usable.
- OS socket buffers/backlog are additionally bounded by the operating system;
  the application does not allocate a parallel worker/thread per connection.

## Tests and review artifacts

```sh
python tools/test_control_bridge.py --output /tmp/ryoko-bridge-evidence
```

This launches an actual Godot subprocess, the actual viewer/rig and TCP clients.
The test-only `tests/control_bridge_host.gd` coordinates local UI signals and
clock snapshots through temporary files, outside the network contract. It is
never loaded by the default app and no testing/file/clock verb exists on the
bridge. The test uses no AI credentials, mock server or remote service.

Evidence includes JSON check results and the Godot process log. Coverage includes
real discovery/control/play/release/reset, strict schema and finite-number
validation, exact atomicity in neutral/manual/performance/release states,
fragmented and pipelined TCP, maximum sizes, duplicate IDs, overload, partial and
idle timeouts, competing clients, reconnect/session fencing, real slider/button/
keyboard takeover, stale queued actions, live-clock playback and clean shutdown.
Run the original rebuild and all Godot/Python suites in `README.md` as well.
Generated logs, reports, captures and cache directories belong outside source.
