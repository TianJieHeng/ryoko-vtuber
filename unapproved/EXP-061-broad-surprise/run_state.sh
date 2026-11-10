#!/bin/sh
# Numerical headless tests only. Native capture requires the supported GUI workflow.
set -eu
W=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
export HOME="$W/local_environment/home" XDG_CACHE_HOME="$W/local_environment/cache" XDG_CONFIG_HOME="$W/local_environment/config" XDG_DATA_HOME="$W/local_environment/data" LP_NUM_THREADS=2
mkdir -p "$HOME" "$XDG_CACHE_HOME" "$XDG_CONFIG_HOME" "$XDG_DATA_HOME"
godot --headless --path "$W/rig" --editor --import > "$W/import.log" 2>&1
godot --headless --path "$W/rig" --script "$W/check_and_capture.gd" > "$W/state.log" 2>&1
godot --headless --path "$W/rig" --script "$W/render_motion.gd" > "$W/motion_state.log" 2>&1
python "$W/verify_preparation.py"
