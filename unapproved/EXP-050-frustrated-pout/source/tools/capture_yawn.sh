#!/bin/bash
set -euo pipefail
PROJECT="$(cd "$(dirname "$0")/.." && pwd)"
OUT="$(realpath -m "${1:-$PROJECT/../review/object}")"
mkdir -p "$OUT" "$OUT/frames" "$OUT/runtime/"{home,config,data,cache}
export HOME="$OUT/runtime/home" XDG_CONFIG_HOME="$OUT/runtime/config" XDG_DATA_HOME="$OUT/runtime/data" XDG_CACHE_HOME="$OUT/runtime/cache"
for n in $(seq 561 579);do if [ ! -e /tmp/.X$n-lock ];then N=$n;break;fi;done
export DISPLAY="localhost:$N" XAUTHORITY="$OUT/runtime/Xauthority"
umask 077;touch "$XAUTHORITY";xauth -f "$XAUTHORITY" add "$DISPLAY" . "$(python -c 'import secrets;print(secrets.token_hex(16))')"
Xorg ":$N" -config "$PROJECT/tools/xorg-mouth-qa.conf" -logfile "$OUT/runtime/Xorg.log" -auth "$XAUTHORITY" -noreset -nolisten unix -nolisten local -listen tcp >"$OUT/runtime/Xorg.stdout" 2>&1 & XPID=$!
trap 'kill "$XPID" 2>/dev/null || true' EXIT
sleep 2;kill -0 "$XPID"
godot --headless --path "$PROJECT" --editor --quit > "$OUT/import.log" 2>&1
godot --path "$PROJECT" --display-driver x11 --rendering-method gl_compatibility --audio-driver Dummy --fixed-fps 30 --write-movie "$OUT/yawn.avi" --script res://review_yawn.gd -- --capture-dir="$OUT/frames" > "$OUT/capture.log" 2>&1
ffmpeg -y -hide_banner -loglevel error -i "$OUT/yawn.avi" -c:v libx264 -crf 17 -pix_fmt yuv420p -movflags +faststart -an "$OUT/ryoko_EXP-163_object_yawn.mp4"
ffprobe -v error -show_entries stream=width,height,r_frame_rate,nb_frames -show_entries format=duration -of json "$OUT/ryoko_EXP-163_object_yawn.mp4" > "$OUT/video_probe.json"
cat "$OUT/video_probe.json"
