#!/bin/bash
set -euo pipefail
PROJECT="$(cd "$(dirname "$0")/.." && pwd)"
TARGET="${1:-$PROJECT}"
OUT="${2:-$PROJECT/../review/mouth_pixel_qa}"
MODE="${3:-}"
RUNTIME="$PROJECT/../runtime/mouth_pixel_qa"
mkdir -p "$OUT" "$RUNTIME/home" "$RUNTIME/config" "$RUNTIME/data" "$RUNTIME/cache"
DISPLAY_NUMBER=""
for number in $(seq 401 499); do
    if [ ! -e "/tmp/.X${number}-lock" ]; then DISPLAY_NUMBER="$number"; break; fi
done
if [ -z "$DISPLAY_NUMBER" ]; then echo "No unused local display" >&2; exit 1; fi
export HOME="$RUNTIME/home" XDG_CONFIG_HOME="$RUNTIME/config" XDG_DATA_HOME="$RUNTIME/data" XDG_CACHE_HOME="$RUNTIME/cache"
export DISPLAY="localhost:$DISPLAY_NUMBER" XAUTHORITY="$RUNTIME/Xauthority$DISPLAY_NUMBER"
umask 077
touch "$XAUTHORITY"
xauth -f "$XAUTHORITY" add "$DISPLAY" . "$(python3 -c 'import secrets; print(secrets.token_hex(16))')"
Xorg ":$DISPLAY_NUMBER" -config "$PROJECT/tools/xorg-mouth-qa.conf" -logfile "$RUNTIME/Xorg$DISPLAY_NUMBER.log" -auth "$XAUTHORITY" -noreset -nolisten unix -nolisten local -listen tcp >"$RUNTIME/Xorg$DISPLAY_NUMBER.stdout" 2>&1 & XPID=$!
trap 'kill "$XPID" 2>/dev/null || true' EXIT
sleep 2
kill -0 "$XPID" 2>/dev/null || { echo "Local display failed" >&2; exit 1; }
godot --headless --path "$TARGET" --editor --quit >"$OUT/import.log" 2>&1
snapshot_inputs() {
python - "$TARGET" "$PROJECT/capture_isolated_mouth_qa.gd" "$1" <<'PY'
import hashlib,json,sys
from pathlib import Path
target=Path(sys.argv[1]); names=['facial_controller.gd','motion_rig.gd','motion_deform.gdshader','expression_deform.gdshaderinc','isolated_mouth.gdshader','expression_performance.gd','expression_performances.json','registration.json','artwork/bust_base.png','artwork/EXP-005_rest_mouth.png','rig_assets/expression_mouths/manifest.json']
manifest=target/'rig_assets/expression_mouths/manifest.json'
if manifest.exists():
    for entry in json.loads(manifest.read_text()).get('profiles',{}).values():
        for key in ('cleared','feature','coverage'):
            if key in entry:
                p='rig_assets/expression_mouths/'+entry[key];names.extend([p,p+'.import'])
result={p:hashlib.sha256((target/p).read_bytes()).hexdigest() for p in names if (target/p).is_file()}
result['capture_script']=hashlib.sha256(Path(sys.argv[2]).read_bytes()).hexdigest()
Path(sys.argv[3]).write_text(json.dumps(result,indent=2)+'\n')
PY
}
snapshot_inputs "$OUT/input_sha256_start.json"
godot --path "$TARGET" --display-driver x11 --rendering-method gl_compatibility --audio-driver Dummy --fixed-fps 30 --script "$PROJECT/capture_isolated_mouth_qa.gd" -- "$(realpath "$OUT")" "$MODE" >"$OUT/capture.log" 2>&1
snapshot_inputs "$OUT/input_sha256_end.json"
cmp "$OUT/input_sha256_start.json" "$OUT/input_sha256_end.json" || { echo "Capture inputs changed during rendering" >&2; exit 1; }
EXTRA=()
if [ -n "${QA_REFERENCE:-}" ]; then EXTRA=(--reference "$QA_REFERENCE"); fi
python "$PROJECT/tools/verify_isolated_mouth_pixels.py" "$OUT" "${EXTRA[@]}" >"$OUT/verify.log" 2>&1
