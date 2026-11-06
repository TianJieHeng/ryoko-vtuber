#!/bin/bash
# Compare an approved v6 input with this project without writing to that input.
set -euo pipefail
PROJECT="$(cd "$(dirname "$0")/.." && pwd)"
BASELINE="$(realpath "${1:?Usage: capture_backbone_parity.sh <approved-v6-project> <external-output-directory>}")"
OUT="$(realpath -m "${2:?Provide an output directory outside both projects}")"
python - "$BASELINE" "$PROJECT" "$OUT" <<'PY'
from pathlib import Path
import shutil,sys
baseline,project,out=map(Path,sys.argv[1:])
assert (baseline/'yawn_rig.gd').is_file(), 'Baseline must be the approved v6 Godot project'
assert out not in (baseline,project) and baseline not in out.parents and project not in out.parents, 'Output must be outside source projects'
assert not (out/'baseline_project').exists(), 'Use a fresh output directory'
out.mkdir(parents=True,exist_ok=True)
shutil.copytree(baseline,out/'baseline_project',ignore=shutil.ignore_patterns('.godot','__pycache__','*.pyc'))
shutil.copyfile(project/'tools/review_backbone_parity.gd',out/'baseline_project/tools/review_backbone_parity.gd')
PY
mkdir -p "$OUT/runtime"/{home,config,data,cache} "$OUT/baseline" "$OUT/candidate"
export HOME="$OUT/runtime/home" XDG_CONFIG_HOME="$OUT/runtime/config" XDG_DATA_HOME="$OUT/runtime/data" XDG_CACHE_HOME="$OUT/runtime/cache"
for n in $(seq 641 659);do if [ ! -e /tmp/.X$n-lock ];then N=$n;break;fi;done
: "${N:?No free Xorg display}"
export DISPLAY="localhost:$N" XAUTHORITY="$OUT/runtime/Xauthority"
umask 077;touch "$XAUTHORITY";xauth -f "$XAUTHORITY" add "$DISPLAY" . "$(python -c 'import secrets;print(secrets.token_hex(16))')"
Xorg ":$N" -config "$PROJECT/tools/xorg-mouth-qa.conf" -logfile "$OUT/runtime/Xorg.log" -auth "$XAUTHORITY" -noreset -nolisten unix -nolisten local -listen tcp >"$OUT/runtime/Xorg.stdout" 2>&1 & XPID=$!
trap 'kill "$XPID" 2>/dev/null || true' EXIT
sleep 2;kill -0 "$XPID"
for variant in baseline candidate;do
 CURRENT="$PROJECT";if [ "$variant" = baseline ];then CURRENT="$OUT/baseline_project";fi
 godot --headless --path "$CURRENT" --editor --quit > "$OUT/$variant/import.log" 2>&1
 godot --path "$CURRENT" --display-driver x11 --rendering-method gl_compatibility --audio-driver Dummy --fixed-fps 30 --script res://tools/review_backbone_parity.gd -- --output="$OUT/$variant" --save-all > "$OUT/$variant/capture.log" 2>&1
 tail -1 "$OUT/$variant/capture.log"
done
python "$PROJECT/tools/compare_backbone_parity.py" "$OUT/baseline" "$OUT/candidate" | tee "$OUT/comparison.json"
