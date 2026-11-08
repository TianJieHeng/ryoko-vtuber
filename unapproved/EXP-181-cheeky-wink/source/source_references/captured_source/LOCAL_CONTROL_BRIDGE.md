# Local external-process control, protocol 1

Twelve user-approved performances share one rig: EXP-163/005/001/006/107/007/002/152/160/177/164/021. EXP-021 Quiet sadness is the approved 3.65-second, five-key data-only performance, available through the existing API and quiet-sadness / quiet_sadness aliases. All eleven predecessor profiles, shared runtime, scenes, shaders and 182 PNGs remain byte-identical to main 2d46f72704ddf2a329b44a87cd24c66d5fe92568. Only EXP-021 profile status changes from its reviewed source; all other fields, times and control values are exact. EXP-003/139/170/153/161 and every other unregistered draft remain excluded.

Current publication checks: python tools/verify_quiet_sadness_publication.py and sha256sum -c SOURCE_FILES.sha256. PUBLICATION_SOURCE_MANIFEST.json is the current manifest. CURRENT_SOURCE_MANIFEST.json, tools/verify_quiet_sadness_package.py, QUIET_SADNESS_CAPTURE_FREEZE.json, historical_capture_metadata/ and inherited exact-scope receipts remain byte-exact historical contracts for their original source trees; do not run them as current publication guards. The historical backbone fixture also remains unchanged and is not a twelve-profile smoke test. Use tests/test_quiet_sadness_runtime.gd for the actual twelve-profile registry. See QUIET_SADNESS_PUBLICATION_VALIDATION.md for scope, evidence and limits.

## Historical EXP-164 publication documentation

Eleven user-approved performances share one rig: EXP-163/005/001/006/107/007/002/152/160/177/164. Fighting sleep adds the approved 3.47-second data-only performance. All ten predecessor profiles, shared runtime, shaders, scenes and 182 PNGs remain byte-identical to main 958eb944a37ce836fec5acf369f12b89f47b6656. Only the EXP-164 profile status text changes from its approved review; all other fields, times, phases and values remain exact. EXP-003/170/139, inner-cover experiments and all other unregistered drafts remain excluded. RELEASE.json and FIGHTING_SLEEP_PUBLICATION_VALIDATION.md record current status. Earlier explicitly marked checkpoints and frozen review receipts are historical provenance. No normal-speed playback observation, AI/TTS or real-socket validation is claimed.

Historical EXP-177 publication checkpoint:

Ten user-approved performances share one rig: EXP-163/005/001/006/107/007/002/152/160/177. Revised EXP-177 Meditative calm adds a single continuous 1.2-second closing arc, with unchanged hold/opening keys from 1.2 seconds onward. All nine prior profiles, gaze_down_extra, rigid outer-anchor brow controls, automatic-blink restoration, runtime and all 182 PNGs remain exact. EXP-003/164 and all other unregistered drafts remain excluded. See MEDITATIVE_PUBLICATION_VALIDATION.md for approval, source identities and verification. Earlier explicitly marked checkpoint descriptions below are historical provenance. The EXP-177 publication profile changes only its status text; every other reviewed field and motion value is exact.

Historical EXP-160 checkpoint: nine user-approved performances shared one rig: EXP-163/005/001/006/107/007/002/152/160. The published002/152 profiles, hidden-iris support and gaze_down_extra semantics are preserved. EXP-160 adds the approved default-zero rigid outer-anchor brow capability without new artwork. EXP-003/177/161/153 remain excluded. See SHY_MERGED_PUBLICATION_VALIDATION.md for merged scope and evidence; preceding frozen review stages are historical.

This is an opt-in local TCP adapter for the default viewer's single shared Godot
rig. The included Python client can run in another process and receive actual
controller results where loopback binding is permitted. Fresh real socket
transport remains unrun for this publication; source/callable tests do not
establish a live connection. No AI model, Ryoko agent service, voice/TTS provider or
lip-sync service is connected. No credentials or persistent authorization are
created. Eleven performances are authored: EXP-163, EXP-005, EXP-001, EXP-006,
EXP-107, EXP-007, EXP-002, EXP-152, EXP-160, EXP-177 and EXP-164. All eleven and their published prerequisites are user-approved; current release status is recorded in `RELEASE.json`.

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

## Historical welcome capability

That scoped extension added `mouth_spread: [0,1]` and the lateral-mouth bounds documented in CONTROL_API.md. At that checkpoint the registered IDs were EXP-163, EXP-005 and EXP-001; the current eleven-ID registry is listed above. There is no wide-eye capability, AI model or TTS connection. Current host socket restrictions prevented rerunning the real loopback suite; its historical receipt must not be presented as a fresh pass.


## Scoped EXP-006 extension

The capability list includes finite normalized `mouth_corner_lift`, `mouth_lip_press` and `blush_intensity`, all defaulting to zero. EXP-006 is discoverable under `giggle` and `suppressed-giggle`. These controls use the existing transaction validator and ownership lifecycle; no new socket, protocol or AI connection is introduced. The blush alpha belongs only to separate FX objects, never the underlying anatomy. Real socket tests must be run where loopback binding is permitted; in-process API checks do not establish network transport success.

## Scoped EXP-107 extension

The existing bridge advertises finite normalized `mouth_oral_lift` [0,1], default zero, and discovers EXP-107 as `confident-reassurance` or `reassure`. It calls the same shared rig. The 40-source-pixel oral-rise envelope and no-AI/no-TTS flags are explicit capabilities. No additional transport is introduced. This sandbox does not permit loopback binding, so fresh real-process socket tests are not claimed; run the included transport test where permitted.

## Scoped EXP-007 rigid purse extension

Capabilities include `mouth_purse` finite [0,1], default 0, and discover EXP-007 (`relieved-smile`, `relief`) through the same registry. The bridge is preparation only. No AI/TTS service is connected, and fresh socket transport remains unrun in this restricted sandbox; source and callable checks do not establish a live client connection.

Auto-blink now preserves an enabled pre-performance preference and restores it after exact neutral recovery. `rig.auto_blink` is the actual state; `rig.auto_blink_pending_restore` is saved intent while performance/release suspends it. `capabilities.auto_blink_policy` documents the policy. Retrigger and repeated release retain intent. Any successful manual write, including `auto_blink:false` while actual blinking is already suspended, cancels deferred restoration and takes ownership immediately. Reset leaves blinking off unless the same transaction explicitly enables it. Completion restarts the existing blink cycle from its open phase. This is local controller preparation, not evidence of a live model, TTS or socket connection. See CONTROL_API.md for exact boundary, pause and no-op semantics.

## Local hidden-cap prerequisite

The callable adapter advertises `gaze_down_extra: [0,1]` and the same additive physical rule as CONTROL_API.md. It forwards the field to the shared controller and does not introduce a separate eye owner. Tests exercise in-process parser/dispatch without starting a listener. Real socket transport, model connections and TTS are not part of this change. The user approved this support with the EXP-152 preview.


## Preserved EXP-002 affectionate warmth

The approved EXP-002 profile, aliases, reference provenance and capture harnesses are retained. Its default gaze_down_extra is zero. The merged runtime uses the reviewed generic gaze capability and all eleven profiles use the same player. See AFFECTION_SCOPE_VALIDATION.md and MERGED_PUBLICATION_VALIDATION.md.


## Approved rigid inner-brow controls

Independent brow_inner_lift_screen_left and brow_inner_lift_screen_right accept finite [0,1], default 0, and add at most 26 degrees after the legacy tilt about fixed outer-tail anchors. Omitted manual fields retain state; omitted timeline fields and reset default to 0. All eleven profiles use the generic player. The gaze_down_extra control remains independent and zero by default. See BROW_INNER_LIFT_VALIDATION.md for exact geometry and historical evidence.

## Approved EXP-177 meditative calm publication

The user-approved revised EXP-177 (meditative-calm / meditate) is the tenth published performance, based on main 70655752bc82ba01b3fe8f64923360da60c578c9. Its single 1.2-second closing arc and all hold/opening motion match the approved review exactly. All nine prior profiles, runtime, artwork, iris/gaze, brow and automatic-blink behavior remain unchanged. RELEASE.json and MEDITATIVE_STATUS.json record current approval/publication. See MEDITATIVE_PUBLICATION_VALIDATION.md. The primary cumulative archive stays at version 19. No normal-speed playback observation, real-socket test or live AI/TTS connection is claimed.

## Approved EXP-164 Fighting sleep publication

The reviewed 3.47-second fifteen-key performance is the eleventh approved entry, using only existing ordinary lids, rigid brows and a restrained sealed purse. The six holds, source-pose relationships and disclosed timing tradeoffs are unchanged. See FIGHTING_SLEEP_PUBLICATION_VALIDATION.md. The current strict successor guard is tools/verify_fighting_sleep_scope.py; inherited exact-scope guards describe historical parent packages and are run only against their exact reconstructed parent. Primary cumulative archive version 19 and original review media/recovery remain untouched.

## Local unapproved independent corners

Capabilities expose `mouth_corner_lift_screen_left/right` in [0,1], default0, and `independent_corners` documents the remaining12px budget. These use the same shared validator; no additional listener or transport is introduced. In-process dispatch is tested separately from real-socket transport, which is not claimed here.
