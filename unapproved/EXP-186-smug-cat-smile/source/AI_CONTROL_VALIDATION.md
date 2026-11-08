# Local control bridge validation

The local bridge connects a separate process to the default viewer's existing
shared controller. It does not connect an AI model, Ryoko agent service, TTS
provider or lip-sync system. No new expression or artwork was authored.

## Current local evidence

- Real Godot 4.6.3 process/socket suite: **317 checks passed**.
- Normal default-app demonstration, without the test host: **8 real successful
  acknowledgments** from a separate standard-library Python client. The yawn
  advanced to 1.50 seconds on the engine clock, then released to neutral and
  reset. No mock server, simulated LLM response or speech-service claim.
- Original generic controller suite: **101890 checks passed**.
- Original base / yawn / teeth Godot suites: **8034 / 55975 / 17017 passed**.
- Original Python base / yawn / teeth source suites: **131 / 29 / 295 passed**
  after regenerating omitted builder diagnostics.
- All **198** previously published project paths retained. All **103** packaged
  PNGs, existing rig/controller/registry code, shaders and approved yawn JSON
  are byte-identical to main `03260259eecc27be25882e42fd66ae99e622ad10`.

The current project keeps prior validation documents in their original context.
Historical source checks mentioning pending art review do not reopen the already
approved yawn, and prior movies are not demonstrations of this new transport.
No new pixel-parity claim is inferred from protocol tests. The unchanged source
hashes and rerun runtime/source suites establish preservation for this phase.

## Coverage and limits

The process suite checks discovery, manual controls, actual controller ownership,
trigger/retrigger/release/reset, frozen-state atomicity in four lifecycle modes,
booleans versus numbers, unknown IDs/fields/verbs, strict JSON, malformed UTF-8,
nonfinite values, nesting/value limits, duplicate keys and request IDs,
fragmented/pipelined/max-size inputs, rate/partial/idle limits, competing clients,
new sessions, manual slider/button/keyboard takeover, stale queued commands,
re-enable, live engine time and process shutdown. Startup without a port, invalid
ports, duplicate launch arguments and conflicting binds are exercised too.

These checks run locally on Linux. The transport/client use cross-platform
Godot/Python APIs, but this report does not claim execution on Windows or macOS.
Loopback does not protect against malicious processes already on the computer.
There is no durable exactly-once guarantee across disconnected sessions and no
implicit release/reset on a connection failure. See `LOCAL_CONTROL_BRIDGE.md`.

Raw logs, full check-by-check JSON, preservation hashes and the actual demo JSONL
are review artifacts outside this source package. Reproduce them with the test
and demo commands in `LOCAL_CONTROL_BRIDGE.md`. Generated diagnostic textures,
movies, logs and caches are not publication inputs. This document records local
validation, not a Git push, CI run, independent audit or user approval of new art.
